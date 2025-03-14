import sqlite3


# Method to perform an SQL query
def sql_query(path, query, params=None):
    print(f"SQL query towards {path}")
    conn = None
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(path)
        cursor = conn.cursor()

        # SQL query to insert data
        insert_query = query

        # Execute the query
        cursor.execute(insert_query, params)
        if not query.strip().lower().startswith("select"):
            # Commit the changes
            conn.commit()
            return cursor.rowcount
        else:
            return cursor.fetchall()

    except sqlite3.Error as e:
        print("Error inserting data:", e)
        return None

    finally:
        # Close the database connection
        if conn:
            conn.close()


# Method to insert a record in the database
def insert_entry(db_path, table_name, record):
    print(f"Insert entry into DB: {db_path}")
    columns = ", ".join(record.keys())
    placeholders = ", ".join(["?"] * len(record))
    params = list(record.values())
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    sql_query(db_path, query, params)
    print("Record inserted successfully!")
    return record


# Method to delete a record from the database
def delete_entry(db_path, table_name, filters):
    print(f"Deleting Record from DB: {db_path}")
    query = f"DELETE FROM {table_name}"
    filter_clauses = []
    params = []

    if filters:
        for it in filters:
            field = it.get("field")
            value = it.get("value")
            if field and value is not None:
                filter_clauses.append(f"{field} = ?")
                params.append(f"{value}")

    # Combine the filter clauses with the base query
    if filter_clauses:
        query += " WHERE " + " AND ".join(filter_clauses)

    result = sql_query(db_path, query, params)

    # Check if any row was deleted
    if result > 0:
        print(f"Entry Successfully deleted.")
        return True
    else:
        print(f"No entries found.")
        return False


# Method to retrieve the records from the database.
def fetch_entries(db_path, table_name, filters=None):
    print(f"Fetching Records from DB: {db_path}")
    records = []
    query = f"SELECT * FROM {table_name}"
    filter_clauses = []
    params = []

    if filters:
        for it in filters:
            field = it.get("field")
            value = it.get("value")
            if field and value is not None:
                filter_clauses.append(f"{field} = ?")
                params.append(f"{value}")

    # Combine the filter clauses with the base query
    if filter_clauses:
        query += " WHERE " + " AND ".join(filter_clauses)

    result = sql_query(db_path, query, params)
    if result is None:
        print("Error: No data found or query failed.")
        return []
    # Convert rows into a list of dictionaries (or tuples) with the column names
    for row in result:
        text, language = row
        records.append({
            "text": text,
            "language": language
        })
    print(f"Records: {records}")
    return records
