from app.db_handler import sql_query, insert_entry, delete_entry, fetch_entries
from unittest.mock import patch, MagicMock


@patch('sqlite3.connect')
def test_sql_query_insert(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1  # Simulate that one row was inserted

    mock_connect.return_value = mock_conn

    query = "INSERT INTO test (text, language) VALUES (?, ?)"
    params = ('racecar', 'English')
    result = sql_query("db", query, params)

    mock_connect.assert_called_once_with("db")
    mock_cursor.execute.assert_called_once_with(query, params)

    assert result == 1


@patch('sqlite3.connect')
def test_sql_query_select(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("racecar", "English"), ("Ana lava lana", "Spanish")]

    mock_connect.return_value = mock_conn

    query = "SELECT * FROM test"
    result = sql_query("db", query)

    mock_connect.assert_called_once_with("db")
    mock_cursor.execute.assert_called_once_with(query, None)

    assert result == [("racecar", "English"), ("Ana lava lana", "Spanish")]


@patch('app.db_handler.sql_query')
def test_insert_entry_success(mock_connect):
    mock_connect.return_value = None

    db_path = "db"
    table_name = "test"
    record = {"text": "racecar", "language": "English"}

    result = insert_entry(db_path, table_name, record)

    query = "INSERT INTO test (text, language) VALUES (?, ?)"
    params = ["racecar", "English"]
    mock_connect.assert_called_once_with(db_path, query, params)

    assert result == record


@patch('app.db_handler.sql_query')
def test_delete_entry_success(mock_connect):
    mock_connect.return_value = 1

    filters = [{"field": "text", "value": "racecar"}, {"field": "language", "value": "English"}]
    db_path = "db"
    table_name = "test"

    query = "DELETE FROM test WHERE text = ? AND language = ?"
    params = ["racecar", "English"]

    result = delete_entry(db_path, table_name, filters)

    mock_connect.assert_called_once_with(db_path, query, params)

    assert result is True


@patch('app.db_handler.sql_query')
def test_delete_entry_no_matching_records(mock_connect):
    mock_connect.return_value = 0

    filters = [{"field": "text", "value": "racecar"}, {"field": "language", "value": "English"}]
    db_path = "db"
    table_name = "test"

    result = delete_entry(db_path, table_name, filters)

    query = "DELETE FROM test WHERE text = ? AND language = ?"
    params = ["racecar", "English"]

    mock_connect.assert_called_once_with(db_path, query, params)

    assert result is False


@patch('app.db_handler.sql_query')
def test_fetch_entries_success_with_filters(mock_connect):
    mock_connect.return_value = [("racecar", "English"), ("Ana lava lana", "Spanish")]

    filters = [{"field": "text", "value": "racecar"}]
    db_path = "db"
    table_name = "test"

    expected_result = [{"text": "racecar", "language": "English"}, {"text": "Ana lava lana", "language": "Spanish"}]

    result = fetch_entries(db_path, table_name, filters)

    mock_connect.assert_called_once_with(db_path, "SELECT * FROM test WHERE text = ?", ["racecar"])
    assert result == expected_result


@patch('app.db_handler.sql_query')
def test_fetch_entries_no_results(mock_connect):
    mock_connect.return_value = None

    filters = [ {"field": "language", "value": "English"}]
    db_path = "db"
    table_name = "test"

    result = fetch_entries(db_path, table_name, filters)

    mock_connect.assert_called_once_with(db_path, "SELECT * FROM test WHERE language = ?", ["English"])

    assert result == []


@patch('app.db_handler.sql_query')
def test_fetch_entries_success_without_filters(mock_connect):
    mock_connect.return_value = [("racecar", "English"), ("Ana lava lana", "Spanish")]

    filters = None
    db_path = "db"
    table_name = "test"

    expected_result = [{"text": "racecar", "language": "English"}, {"text": "Ana lava lana", "language": "Spanish"}]

    result = fetch_entries(db_path, table_name, filters)

    mock_connect.assert_called_once_with(db_path, "SELECT * FROM test", [])
    assert result == expected_result

