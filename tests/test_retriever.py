
from backend.database import (
    get_connection,
    initialize_database,
    save_document,
    save_chunk,
)
from backend.embeddings import create_embedding
from backend.retriever import retrieve_relevant_chunks


def test_retrieve_relevant_chunks():
    initialize_database()

    filename = "retriever_test.txt"

    with get_connection() as connection:
        old_documents = connection.execute(
            "SELECT id FROM documents WHERE filename = ?",
            (filename,),
        ).fetchall()

        for document in old_documents:
            connection.execute(
                "DELETE FROM document_chunks WHERE document_id = ?",
                (document["id"],),
            )

        connection.execute(
            "DELETE FROM documents WHERE filename = ?",
            (filename,),
        )

    text = "Python is a programming language."

    document_id = save_document(
        filename,
        "data/uploads/retriever_test.txt",
        text,
    )

    embedding = create_embedding(text)

    save_chunk(
        document_id,
        text,
        embedding,
    )

    results = retrieve_relevant_chunks(
        "What is Python?",
        top_k=1,
    )

    assert len(results) == 1
    assert results[0]["filename"] == filename
    assert "Python" in results[0]["text"]
    assert results[0]["similarity"] > 0.5
