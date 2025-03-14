from app.db_handler import delete_entry
from app.db_handler import insert_entry
from app.db_handler import fetch_entries
from app.util import is_palindrome
from app.palindrome import Palindrome
from typing import Optional

DB_PATH = "/app/palindromes.db"
TABLE_NAME = "palindromes"


# Business logic method to add a palindrome record
def add_record(palindrome):
    return insert_entry(DB_PATH, TABLE_NAME, palindrome)


# Business logic method to delete a palindrome record
def delete_record(language: Optional[str], text: Optional[str]):
    print("Delete Record Controller")
    filters = []
    if not language or not text:
        print("Invalid filter type. Use 'language' and 'text'.")
        return

    if language:
        filters.append({"field": "language", "value": language})
    if text:
        filters.append({"field": "text", "value": text})

    return delete_entry(DB_PATH, TABLE_NAME, filters)


# Business logic method to retrieve palindrome records
def get_records(text: Optional[str], language: Optional[str]):
    print("Get Records Controller")
    filters = []
    if text:
        filters.append({"field": "text", "value": text})
    if language:
        filters.append({"field": "language", "value": language})

    records = fetch_entries(DB_PATH, TABLE_NAME, filters)
    return records


# Business logic method to validate if a request contains a palindrome
def validate_record(body):
    print("Validate record")
    string = body.get("text")
    if is_palindrome(string) is True:
        record = Palindrome(*body.values())
        print(f"Text {record.text} is a Palindrome. Adding to the DB")
        add_record(record)
        return record.get()
    else:
        print(f"Text {string} is not a Palindrome.")
        return None
