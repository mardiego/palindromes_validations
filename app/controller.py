from app.db_handler import delete_entry
from app.db_handler import insert_entry
from app.db_handler import fetch_entries
from app.util import is_palindrome
from app.palindrome import Palindrome as Palindrome
from typing import Optional


# Business logic to add a palindrome record
def add_record(palindrome):
    return insert_entry(palindrome)


# Business logic to delete a palindrome record
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
    return delete_entry(filters)


# Business logic to retrieve palindrome records
def get_records(text: Optional[str], language: Optional[str]):
    print("Get Records Controller")
    filters = []
    if text:
        filters.append({"field": "text", "value": text})
    if language:
        filters.append({"field": "language", "value": language})

    records = fetch_entries(filters)
    return records


# Business logic to validate if a request contains a palindrome
def validate_record(body):
    print("Validate record")
    record = Palindrome(*body.values())
    if is_palindrome(record.text) is True:
        print(f"Text {record.text} is a Palindrome. Adding to the DB")
        return add_record(record)
    else:
        print(f"Text {record.text} is not a Palindrome.")
        return None
