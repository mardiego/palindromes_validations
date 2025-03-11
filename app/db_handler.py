import sqlite3

DB_PATH = "/app/palindromes.db"


# Method to delete a record from the database
def delete_entry(filters):
    print(f"Deleting Record from DB: {DB_PATH}")
    conn = None
    query = "DELETE FROM records"
    filter_clauses = []
    params = []

    if filters:
        for filter in filters:
            field = filter.get("field")
            value = filter.get("value")
            # Add the appropriate WHERE condition based on the field
            if field == "text":
                filter_clauses.append("text = ?")
                params.append(f"{value}")
            elif field == "language":
                filter_clauses.append("language = ?")
                params.append(f"{value}")

    # Combine the filter clauses with the base query
    if filter_clauses:
        query += " WHERE " + " AND ".join(filter_clauses)

    try:
        # Connect to SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if not filter_clauses:
            print("Invalid filter type. Use 'language' or 'text'.")
            return
        print(f"SQL Query {query}")
        # SQL query to select all rows from the jobs table
        cursor.execute(query, params)

        # Commit the changes
        conn.commit()

        # Check if any row was deleted
        if cursor.rowcount > 0:
            print(f"Entry Successfully deleted.")
            return True
        else:
            print(f"No entries found.")
            return False

    except sqlite3.Error as e:
        print("Error deleting record:", e)
        return None

    finally:
        # Close the database connection
        if conn:
            conn.close()