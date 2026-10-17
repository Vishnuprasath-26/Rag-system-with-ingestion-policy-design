# Intelligent RAG System with Ingestion Policy Engine

## 1. Project Overview

The Intelligent RAG System is a document-based question-answering application that uses Retrieval-Augmented Generation (RAG).

Users can upload documents, validate them against ingestion policies, extract their text, divide the text into chunks, generate embeddings, and store the data in an SQLite database.

When a user asks a question, the system retrieves relevant document chunks using semantic similarity and sends the retrieved context to a locally running Ollama language model to generate an answer.

## 2. Features

- Document upload for PDF, DOCX, and TXT files.
- File validation using ingestion policies.
- File size and filename validation.
- Text extraction from supported documents.
- Text chunking with overlapping sections.
- Semantic embeddings using Sentence Transformers.
- SQLite storage for documents, chunks, and embeddings.
- Similarity-based document retrieval.
- Question answering using a local Ollama model.
- REST API built with FastAPI.
- API testing through Swagger UI.
- Document listing and deletion.

## 3. Technology Stack

- **Language:** Python
- **API Framework:** FastAPI
- **API Testing:** Swagger UI
- **Database:** SQLite
- **Embeddings:** Sentence Transformers
- **Embedding Model:** sentence-transformers/all-MiniLM-L6-v2
- **Language Model:** Ollama with llama3.2
- **Document Processing:** pypdf and python-docx
- **Numerical Processing:** NumPy

## 4. Project Structure

```text
Rag system with ingestion policy design/
|
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── policy.py
│   ├── extractor.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── database.py
│   ├── retriever.py
│   └── llm.py
|
├── data/
│   └── uploads/
|
├── tests/
|
├── .venv/
└── README.md
```

This is the expected structure based on the modules developed for the project. Adjust it if your actual folders differ.

## 5. Installation

Open PowerShell and navigate to the project folder:

```powershell
cd "C:\Users\HP\Downloads\Rag system with ingestion policy design"
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```powershell
python -m pip install fastapi uvicorn python-multipart pydantic requests numpy sentence-transformers pypdf python-docx pytest
```

Make sure Ollama is installed and the required model is available:

```powershell
ollama pull llama3.2
```

## 6. Run the Application

Start the FastAPI server:

```powershell
python -m uvicorn backend.main:app --reload
```

Open the API documentation in your browser:

http://127.0.0.1:8000/docs

## 7. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check application status |
| POST | `/documents/upload` | Upload and process a document |
| GET | `/documents` | List uploaded documents |
| DELETE | `/documents/{document_id}` | Delete a document |
| POST | `/ask` | Ask a question about uploaded documents |

## 8. How RAG Works

1. A user uploads a document.
2. The ingestion policy validates the filename, extension, and file size.
3. The extraction module extracts readable text.
4. The chunker divides the text into smaller overlapping sections.
5. The embedding model converts each chunk into a numerical vector.
6. SQLite stores the document, chunks, and embeddings.
7. A user submits a question.
8. The system generates an embedding for the question.
9. The retriever compares the question vector with stored chunk vectors.
10. Relevant chunks are passed to Ollama as context.
11. The language model generates an answer based on the retrieved context.
12. The API returns the answer and source information.

## 9. Run Tests

Run the test suite:

```powershell
python -m pytest -v
```

Review the output to confirm which tests pass and which need fixing.

## 10. Future Improvements

- Configurable ingestion policies.
- Authentication and role-based access control.
- Improved logging and monitoring.
- More robust document parsing and OCR support.
- Document-level access permissions.
- Better retrieval evaluation and tuning.
- Automated API and integration tests.
- A user-friendly frontend.

## 11. Project Goal

The goal is to build a local document intelligence system that combines controlled document ingestion, semantic retrieval, and context-based question answering while keeping the language model running locally.
