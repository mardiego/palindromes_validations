from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch

client = TestClient(app)

@patch("app.main.validate_record")
def test_validate_palindromes_success(mock_validate_record):
    mock_validate_record.return_value = "Palindrome racecar has been successfully added"
    response = client.post("/palindromes/validate_palindromes", json={"language": "English", "text": "racecar"})
    assert response.status_code == 201
    assert response.json() == {"response" : "Palindrome racecar has been successfully added"}

@patch("app.main.validate_record")
def test_validate_palindromes_no_palindrome(mock_validate_record):
    mock_validate_record.return_value = None
    response = client.post("/palindromes/validate_palindromes", json={"language": "English", "text": "hello"})
    assert response.status_code == 400
    assert response.json() == {"detail" : "Not a palindrome"}

def test_validate_palindromes_server_error():
    response = client.post("/palindromes/validate_palindromes", json={"trigger_error": True})
    assert response.status_code == 500
    assert response.json() == {"detail" : "An error occurred while processing the request"}

@patch("app.main.get_records")
def test_get_palindromes_success(mock_get_records):
    mock_get_records.return_value = {"language": "en", "text": "non_palindrome"}
    response = client.get("/palindromes/get_palindromes", params={"language": "en", "text": "racecar"})
    assert response.status_code == 200
    assert response.json() == {"response" : "Palindromes records matching filter", "Palindromes":  {"language": "en", "text": "non_palindrome"}}

@patch("app.main.get_records")
def test_get_palindromes_not_found(mock_get_records):
    mock_get_records.return_value = None
    response = client.get("/palindromes/get_palindromes", params={"language": "en", "text": "non_palindrome"})
    assert response.status_code == 404
    assert response.json() == {"detail" : "No Palindromes found"}

@patch("app.main.get_records")
def test_get_palindromes_server_error(mock_get_records):
    def mock_get_records_error(text, language):
        raise Exception("Unexpected error")
    mock_get_records.side_effect = mock_get_records_error
    response = client.get("/palindromes/get_palindromes")
    assert response.status_code == 500
    assert response.json() == {"detail" : "An error occurred while processing the request"}

@patch("app.main.delete_record")
def test_delete_palindromes_success(mock_delete_record):
    mock_delete_record.return_value = True
    response = client.delete("/palindromes/delete_palindromes", params={"language": "en", "text": "racecar"})
    assert response.status_code == 200
    assert response.json() == {"response" : "Entry successfully deleted"}

@patch("app.main.delete_record")
def test_delete_palindromes_no_content(mock_delete_record):
    mock_delete_record.return_value = False
    response = client.delete("/palindromes/delete_palindromes", params={"language": "en", "text": "non_palindrome"})
    assert response.status_code == 204
    assert response.text == ""

@patch("app.main.delete_record")
def test_delete_palindromes_bad_request(mock_delete_record):
    mock_delete_record.return_value = None
    response = client.delete("/palindromes/delete_palindromes")
    assert response.status_code == 422

@patch("app.main.delete_record")
def test_delete_palindromes_server_error(mock_delete_record):
    def mock_delete_records_error(text, language):
        raise Exception("Unexpected error")
    mock_delete_record.side_effect = mock_delete_records_error
    response = client.delete("/palindromes/delete_palindromes", params={"language": "en", "text": "racecar"})
    assert response.status_code == 500
    assert response.json() == {"detail" : "An error occurred while processing the request"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
