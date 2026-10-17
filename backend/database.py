
import json
import sqlite3

from backend.config import PROJECT_ROOT


DATABASE_PATH = PROJECT_ROOT / "data" / "rag_system.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                extracted_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS document_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                chunk_text TEXT NOT NULL,
                embedding TEXT NOT NULL,
                FOREIGN KEY (document_id)
                    REFERENCES documents(id)
                    ON DELETE CASCADE
            )
            """
        )


def save_document(
    filename: str,
    file_path: str,
    extracted_text: str,
) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO documents (
                filename,
                file_path,
                extracted_text
            )
            VALUES (?, ?, ?)
            """,
            (filename, file_path, extracted_text),
        )

        return cursor.lastrowid


def save_chunk(
    document_id: int,
    chunk_text: str,
    embedding: list[float],
):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO document_chunks (
                document_id,
                chunk_text,
                embedding
            )
            VALUES (?, ?, ?)
            """,
            (
                document_id,
                chunk_text,
                json.dumps(embedding),
            ),
        )


def save_document_with_chunks(
    filename: str,
    file_path: str,
    extracted_text: str,
    chunks: list[str],
    embeddings: list[list[float]],
) -> int:
    if len(chunks) != len(embeddings):
        raise ValueError(
            "The number of chunks must match the number of embeddings."
        )

    if not chunks:
        raise ValueError("At least one chunk is required.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO documents (
                filename,
                file_path,
                extracted_text
            )
            VALUES (?, ?, ?)
            """,
            (filename, file_path, extracted_text),
        )

        document_id = cursor.lastrowid

        connection.executemany(
            """
            INSERT INTO document_chunks (
                document_id,
                chunk_text,
                embedding
            )
            VALUES (?, ?, ?)
            """,
            [
                (
                    document_id,
                    chunk,
                    json.dumps(embedding),
                )
                for chunk, embedding in zip(chunks, embeddings)
            ],
        )

        return document_id


def get_all_documents() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                filename,
                created_at,
                LENGTH(extracted_text) AS text_length
            FROM documents
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def delete_document(document_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM documents WHERE id = ?",
            (document_id,),
        )

        return cursor.rowcount > 0
