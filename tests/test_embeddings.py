
from backend.embeddings import create_embedding, create_embeddings


def test_single_embedding():
    result = create_embedding("The company provides financial services.")

    assert len(result) == 384
    assert all(isinstance(value, float) for value in result)


def test_multiple_embeddings():
    results = create_embeddings(["Hello world", "Document search"])

    assert len(results) == 2
    assert all(len(result) == 384 for result in results)


def test_empty_list():
    assert create_embeddings([]) == []
