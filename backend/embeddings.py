
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def create_embedding(text: str) -> list[float]:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    embedding = model.encode(text, normalize_embeddings=True)

    return embedding.tolist()


def create_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    if any(not text.strip() for text in texts):
        raise ValueError("Texts cannot contain empty strings.")

    embeddings = model.encode(texts, normalize_embeddings=True)

    return embeddings.tolist()
