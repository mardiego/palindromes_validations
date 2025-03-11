from app.db_handler import delete_entry
from typing import Optional


def delete_record(language: Optional[str], text: Optional[str]):
    print("Delete Record Controller")
    filters = []
    if language:
        filters.append({"field": "language", "value": language})
    if text:
        filters.append({"field": "text", "value": text})

    if not filters:
        print("Invalid filter type. Use 'language' and/or 'text'.")
        return
    return delete_entry(filters)

