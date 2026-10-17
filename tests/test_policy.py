
from backend.policy import validate_document


def test_valid_pdf():
    valid, message = validate_document("sample.pdf", 1024)
    assert valid is True


def test_valid_txt():
    valid, message = validate_document("sample.txt", 1024)
    assert valid is True


def test_invalid_extension():
    valid, message = validate_document("sample.exe", 1024)
    assert valid is False


def test_empty_file():
    valid, message = validate_document("sample.pdf", 0)
    assert valid is False


def test_file_too_large():
    valid, message = validate_document("sample.pdf", 6 * 1024 * 1024)
    assert valid is False


def test_empty_filename():
    valid, message = validate_document("", 1024)
    assert valid is False


def test_filename_with_path():
    valid, message = validate_document("../sample.pdf", 1024)
    assert valid is False
