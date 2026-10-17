
from backend.chunker import chunk_text


def test_empty_text():
    assert chunk_text("") == []


def test_short_text():
    assert chunk_text("one two three") == ["one two three"]


def test_text_is_split():
    text = " ".join(f"word{i}" for i in range(450))
    chunks = chunk_text(text, chunk_size=200, overlap=40)

    assert len(chunks) == 3
    assert len(chunks[0].split()) == 200
    assert len(chunks[1].split()) == 200
    assert len(chunks[2].split()) == 130


def test_invalid_overlap():
    try:
        chunk_text("hello world", chunk_size=10, overlap=10)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
