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
    connection.execute(
    """
    INSERT INTO companies (name, country)
    VALUES (?, ?)
    """, 
    (name, country),
    )
    connection.commit()
    
def get_companies(connection: sqlite3.Connection) -> list[tuple]:
    cursor = connection.execute("SELECT id, name, country FROM companies")
    companies = cursor.fetchall()
    return companies

def delete_company(connection: sqlite3.Connection, company_id: int) -> None:
    connection.execute("DELETE FROM companies WHERE id = ?",(company_id,),)
    connection.commit()

def update_company (connection:sqlite3.Connection, company_id : int,name : str,country : str) -> None:
    connection.execute(
    """
    UPDATE companies
    SET name = ?, country = ?
    WHERE id = ?
    """,
    (name, country, company_id),
    )
    connection.commit()

def company_exists(connection: sqlite3.Connection,name: str,country: str,) -> bool:
    cursor = connection.execute(
        """
        SELECT id
        FROM companies
        WHERE LOWER(name) = LOWER(?)
          AND LOWER(country) = LOWER(?)
        """,
        (name, country),
    )

    return cursor.fetchone() is not None

def search_companies(connection: sqlite3.Connection,search_term: str,) -> list[tuple]:
    cursor = connection.execute(
        """
        SELECT id, name, country
        FROM companies
        WHERE LOWER(name) LIKE LOWER(?)
        ORDER BY name
        """,
        (f"%{search_term}%",),
    )
    return cursor.fetchall()