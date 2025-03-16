from app.controller import delete_record
from app.controller import get_records
from app.controller import add_record
from app.controller import validate_record
from app.palindrome import Palindrome
from unittest.mock import patch


def test_delete_record_invalid_filters(capfd):
    result = delete_record(None, None)
    captured = capfd.readouterr()

    assert "Invalid filter type. Use 'language' and 'text'." in captured.out
    assert result is None


def test_delete_record_invalid_language(capfd):
    result = delete_record(None, "racecar")
    captured = capfd.readouterr()

    assert "Invalid filter type. Use 'language' and 'text'." in captured.out
    assert result is None


def test_delete_record_invalid_text(capfd):
    result = delete_record("English", None)
    captured = capfd.readouterr()

    assert "Invalid filter type. Use 'language' and 'text'." in captured.out
    assert result is None


@patch("app.controller.delete_entry")
def test_delete_record_valid(mock_delete_entry):
    mock_delete_entry.return_value = True
    db_path = "/app/palindromes.db"
    table_name = "palindromes"
    result = delete_record("English", "racecar")

    mock_delete_entry.assert_called_once_with(db_path, table_name, [
        {"field": "language", "value": "English"},
        {"field": "text", "value": "racecar"}
    ])

    assert result == True


@patch("app.controller.fetch_entries")
def test_get_records_with_no_filters(mock_fetch_entries):
        mock_fetch_entries.return_value = []
        db_path = "/app/palindromes.db"
        table_name = "palindromes"
        result = get_records(None, None)
        mock_fetch_entries.assert_called_once_with(db_path, table_name, [])

        assert result == []


@patch("app.controller.fetch_entries")
def test_get_records_with_text_filter(mock_fetch_entries):
    mock_fetch_entries.return_value = []
    db_path = "/app/palindromes.db"
    table_name = "palindromes"
    result = get_records("racecar", None)
    mock_fetch_entries.assert_called_once_with(db_path, table_name, [{"field": "text", "value": "racecar"}])

    assert result == []


@patch("app.controller.fetch_entries")
def test_get_records_with_language_filter(mock_fetch_entries):
    mock_fetch_entries.return_value = []
    db_path = "/app/palindromes.db"
    table_name = "palindromes"
    result = get_records(None, "English")
    mock_fetch_entries.assert_called_once_with(db_path, table_name, [{"field": "language", "value": "English"}])

    assert result == []


@patch("app.controller.insert_entry")
def test_add_record(mock_insert_entry):
    palindrome = Palindrome("racecar", "English")
    mock_insert_entry.return_value = "Palindrome racecar has been successfully added"
    db_path = "/app/palindromes.db"
    table_name = "palindromes"
    result = add_record(palindrome)
    mock_insert_entry.assert_called_once_with(db_path, table_name, palindrome)
    assert result == mock_insert_entry.return_value


@patch("app.controller.add_record")
def test_validate_record_valid(mock_add_record):
    body = {"text": "racecar", "language": "English"}
    mock_add_record.return_value = "Palindrome racecar has been successfully added"
    result = validate_record(body)
    assert result == mock_add_record.return_value


@patch("app.controller.add_record")
def test_validate_record_invalid(mock_add_record):
    body = {"text": "hello", "language": "English"}
    mock_add_record.return_value = None
    result = validate_record(body)
    assert result == mock_add_record.return_value
