
from backend.llm import generate_answer


def test_empty_context():
    answer = generate_answer(
        "What is Python?",
        "",
    )

    assert "could not find" in answer.lower()


def test_empty_question():
    try:
        generate_answer(
            "",
            "Python is a programming language.",
        )
    except ValueError as error:
        assert "Question cannot be empty" in str(error)
    else:
        raise AssertionError("Expected ValueError")
