from database import create_connection, create_companies_table


connection = create_connection()

create_companies_table(connection)

print("Companies table is ready.")

connection.close()