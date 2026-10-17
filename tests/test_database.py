
from backend.database import (
    get_connection,
    initialize_database,
    save_document,
    save_chunk,
)


def test_save_document_and_chunk():
    initialize_database()

    document_id = save_document(
        "sample.txt",
        "data/uploads/sample.txt",
        "This is sample document text.",
    )

    save_chunk(
        document_id,
        "This is sample document text.",
        [0.1, 0.2, 0.3],
    )

    with get_connection() as connection:
        document = connection.execute(
            "SELECT * FROM documents WHERE id = ?",
            (document_id,),
        ).fetchone()

        chunk = connection.execute(
            "SELECT * FROM document_chunks WHERE document_id = ?",
            (document_id,),
        ).fetchone()

    assert document is not None
    assert document["filename"] == "sample.txt"
    assert chunk is not None
    assert chunk["chunk_text"] == "This is sample document text."
