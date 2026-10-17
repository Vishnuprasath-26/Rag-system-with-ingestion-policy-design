
import json

import numpy as np

from backend.database import get_connection
from backend.embeddings import create_embedding


def retrieve_relevant_chunks(
    question: str,
    top_k: int = 3,
    similarity_threshold: float = 0.35,
) -> list[dict]:
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if not -1.0 <= similarity_threshold <= 1.0:
        raise ValueError(
            "similarity_threshold must be between -1 and 1."
        )

    question_embedding = np.array(
        create_embedding(question),
        dtype=np.float32,
    )

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                document_chunks.id AS chunk_id,
                document_chunks.document_id,
                document_chunks.chunk_text,
                document_chunks.embedding,
                documents.filename
            FROM document_chunks
            JOIN documents
                ON documents.id = document_chunks.document_id
            """
        ).fetchall()

    results = []

    for row in rows:
        stored_embedding = np.array(
            json.loads(row["embedding"]),
            dtype=np.float32,
        )

        if stored_embedding.shape != question_embedding.shape:
            continue

        similarity = float(
            np.dot(question_embedding, stored_embedding)
        )

        if similarity < similarity_threshold:
            continue

        results.append(
            {
                "chunk_id": row["chunk_id"],
                "document_id": row["document_id"],
                "filename": row["filename"],
                "text": row["chunk_text"],
                "similarity": similarity,
            }
        )

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    return results[:top_k]
