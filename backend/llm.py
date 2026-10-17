
import requests

from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL


def generate_answer(question: str, context: str) -> str:
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if not context or not context.strip():
        return "I could not find relevant information in the uploaded documents."

    prompt = f"""
You are a helpful document question-answering assistant.

Answer the question using only the provided context.
Do not invent facts or use information outside the context.
If the answer is not available in the context, clearly say so.

Context:
{context}

Question:
{question}

Answer:
"""

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()

    except requests.RequestException as error:
        raise RuntimeError(
            "Could not connect to Ollama. Make sure Ollama is running "
            "and the configured model is installed."
        ) from error

    answer = response.json().get("response", "").strip()

    if not answer:
        raise RuntimeError("Ollama returned an empty answer.")

    return answer
