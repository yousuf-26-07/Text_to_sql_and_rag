import sqlite3
from config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def run_query(sql):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()

    conn.close()

    return rows

def get_schema():

    conn = get_connection()
    cursor = conn.cursor()

    schema = ""

    tables = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()

    for table in tables:

        table_name = table[0]

        columns = cursor.execute(
            f"PRAGMA table_info({table_name});"
        ).fetchall()

        column_names = [col[1] for col in columns]

        schema += f"Table: {table_name}\nColumns: {', '.join(column_names)}\n\n"

    conn.close()

    return schema