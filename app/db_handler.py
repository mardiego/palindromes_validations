import sqlite3

DB_PATH = "/app/palindromes.db"


# Function to insert a record in the database
def insert_entry(record):
    conn = None
    print(f"Database path: {DB_PATH}")
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # SQL query to insert data
        insert_query = """
            INSERT INTO records (text, language) 
            VALUES (?, ?)
            """
        # Execute the query
        cursor.execute(insert_query, (record.text, record.language))
        # Commit the changes
        conn.commit()
        print("Record inserted successfully!")
        return record.get()

    except sqlite3.Error as e:
        print("Error inserting data:", e)
        return f"Error inserting data: {e}"

    finally:
        # Close the database connection
        if conn:
            conn.close()


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
        # SQL query to delete a record from the table
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


# Function to retrieve the records from the database.
def fetch_entries(filters=None):
    print(f"Fetching Record from DB: {DB_PATH}")
    conn = None
    records = []
    query = "SELECT * FROM records"
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
        # SQL query to select all records from the DB
        cursor.execute(query, params)
        # Fetch all rows
        rows = cursor.fetchall()
        # Convert rows into a list of dictionaries (or tuples) with the column names
        for row in rows:
            text, language = row
            records.append({
                "text": text,
                "language": language
            })

    except sqlite3.Error as e:
        print(f" Error fetching data: {e}")

    finally:
        if conn:
            conn.close()

    return records
