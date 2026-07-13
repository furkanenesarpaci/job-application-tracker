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

def add_company(connection: sqlite3.Connection, name: str, country: str) -> None:
    connection.execute("""
        INSERT INTO companies (name, country)
        VALUES (?, ?)
    """, (name, country))
    connection.commit()
    
def get_companies(connection: sqlite3.Connection) -> list[tuple]:
    cursor = connection.execute("SELECT id, name, country FROM companies")
    companies = cursor.fetchall()
    return companies

def delete_company(connection: sqlite3.Connection, company_id: int) -> None:
        connection.execute("DELETE FROM companies WHERE id = ?",(company_id,),)
        connection.commit()
