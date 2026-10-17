
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from backend.chunker import chunk_text
from backend.config import UPLOAD_DIR
from backend.database import (
    delete_document,
    get_all_documents,
    get_connection,
    initialize_database,
    save_document_with_chunks,
)
from backend.embeddings import create_embeddings
from backend.extractor import extract_text
from backend.llm import generate_answer
from backend.policy import validate_document
from backend.retriever import retrieve_relevant_chunks


app = FastAPI(
    title="Intelligent RAG System",
    description=(
        "Document ingestion, policy validation, "
        "semantic retrieval, and question answering"
    ),
    version="1.0.0",
)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=3, ge=1, le=10)
    similarity_threshold: float = Field(
        default=0.35,
        ge=-1.0,
        le=1.0,
    )


@app.on_event("startup")
def startup():
    initialize_database()
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Intelligent RAG System is running"
    }


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename or ""
    content = await file.read()

    valid, message = validate_document(
        filename,
        len(content),
    )

    if not valid:
        await file.close()
        raise HTTPException(
            status_code=400,
            detail=message,
        )

    safe_filename = Path(filename).name
    extension = Path(safe_filename).suffix.lower()
    stored_filename = f"{uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / stored_filename

    try:
        file_path.write_bytes(content)

        extracted_text = extract_text(file_path)
        chunks = chunk_text(extracted_text)

        if not chunks:
            raise ValueError(
                "No text chunks were created."
            )

        embeddings = create_embeddings(chunks)

        document_id = save_document_with_chunks(
            safe_filename,
            str(file_path),
            extracted_text,
            chunks,
            embeddings,
        )

        return {
            "message": (
                "Document uploaded and processed successfully"
            ),
            "document_id": document_id,
            "filename": safe_filename,
            "chunks_created": len(chunks),
        }

    except HTTPException:
        file_path.unlink(missing_ok=True)
        raise

    except Exception:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=(
                "Document processing failed. "
                "Check the server logs for details."
            ),
        ) from None

    finally:
        await file.close()


@app.get("/documents")
def list_documents():
    return {
        "documents": get_all_documents()
    }


@app.delete("/documents/{document_id}")
def remove_document(document_id: int):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT file_path
            FROM documents
            WHERE id = ?
            """,
            (document_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    deleted = delete_document(document_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    try:
        Path(row["file_path"]).unlink(missing_ok=True)
    except OSError:
        raise HTTPException(
            status_code=500,
            detail=(
                "Document record was deleted, but the uploaded "
                "file could not be removed."
            ),
        ) from None

    return {
        "message": (
            "Document and its associated chunks "
            "deleted successfully"
        ),
        "document_id": document_id,
    }


@app.post("/ask")
def ask_question(request: AskRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        retrieved_chunks = retrieve_relevant_chunks(
            question,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold,
        )

        context = "\n\n".join(
            chunk["text"]
            for chunk in retrieved_chunks
        )

        answer = generate_answer(
            question,
            context,
        )

        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "document_id": chunk["document_id"],
                    "filename": chunk["filename"],
                    "chunk_id": chunk["chunk_id"],
                    "similarity": round(
                        chunk["similarity"],
                        4,
                    ),
                }
                for chunk in retrieved_chunks
            ],
        }

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from None

    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "Question answering failed due to "
                "an internal error."
            ),
        ) from None
