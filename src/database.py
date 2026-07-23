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

def create_applications_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            position TEXT NOT NULL,
            status TEXT NOT NULL,
            applied_at TEXT NOT NULL,
            FOREIGN KEY (company_id) REFERENCES companies (id)
        )
        """
    )
    connection.commit()

def add_application(
    connection: sqlite3.Connection,
    company_id: int,
    position: str,
    status: str,
    applied_at: str,
) -> None:
    connection.execute(
        """
        INSERT INTO applications (
            company_id,
            position,
            status,
            applied_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (company_id, position, status, applied_at),
    )
    connection.commit()

def get_applications(connection: sqlite3.Connection,) -> list[tuple]:
        
    cursor = connection.execute(
        """
        SELECT
            applications.id,
            companies.name,
            applications.position,
            applications.status,
            applications.applied_at
        FROM applications
        JOIN companies
            ON applications.company_id = companies.id
        ORDER BY applications.id
        """
    )
    return cursor.fetchall()

def update_application(
    connection: sqlite3.Connection,
    application_id: int,
    position: str,
    status: str,
) -> None:
    connection.execute(
        """
        UPDATE applications
        SET position = ?, status = ?
        WHERE id = ?
        """,
        (position, status, application_id),
    )
    connection.commit()