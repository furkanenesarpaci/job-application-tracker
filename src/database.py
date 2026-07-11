import sqlite3


def create_connection() -> sqlite3.Connection:
    connection = sqlite3.connect("job_tracker.db")
    return connection


def create_companies_table(connection: sqlite3.Connection) -> None:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL
        )
    """)
    connection.commit()