from datetime import date
from database import add_company
from database import create_companies_table
from database import update_company
from database import create_connection
from database import get_companies
from database import delete_company
from database import company_exists
from database import search_companies
from database import create_applications_table
from database import add_application


def show_menu() -> None:
    print("\n1. Add company")
    print("2. List companies")
    print("3. Delete company")
    print("4. Update company")
    print("5. Search company")
    print("6. Add application")
    print("0. Exit")


connection = create_connection()


try:
    create_companies_table(connection)
    create_applications_table(connection)

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            company_name = input("Company name: ").strip()
            company_country = input("Company country: ").strip()

            if company_name == "" or company_country == "":
                print("Company name and country cannot be empty.")

            elif company_exists(connection, company_name, company_country):
                print("This company already exists.")
            else:
                add_company(connection, company_name, company_country)
                print("Company added.")

        elif choice == "2":
            companies = get_companies(connection)

            for company in companies:
                print(company)
        
        elif choice == "3":
            companies = get_companies(connection)
            
            for company in companies:
                print(company)

            while True:
                company_id = input("Enter the ID of the company you want to delete,(0 for menu) ").strip()
                
                if company_id == "0":
                    break
                
                if company_id.isdigit():
                    valid_ids = []
                    for company in companies:
                        valid_ids.append(str(company[0]))
                    
                    if company_id in valid_ids:
                        delete_company(connection,int(company_id))
                        print(f"Company number {company_id} is deleted")
                        break
                    else :
                        print("There is no company with this ID.")
                else:
                    print("Company ID must be a number")

        elif choice == "4":
            companies = get_companies(connection)

            for company in companies:
                print(company)

            while True:
                company_id = input(
                    "Select the company ID you want to update (0 for menu): "
                ).strip()

                if company_id == "0":
                    break

                valid_ids = []

                for company in companies:
                    valid_ids.append(str(company[0]))

                if company_id not in valid_ids:
                    print("There is no company with this ID.")
                    continue

                new_name = input("Enter the new name: ").strip()
                new_country = input("Enter the new country: ").strip()

                if new_name == "" or new_country == "":
                    print("Company name and country cannot be empty.")
                    continue

                update_company(
                    connection,
                    int(company_id),
                    new_name,
                    new_country,
                )

                print(f"Company number {company_id} is updated.")
                break
        
        elif choice == "5":
            while True:
                    search_term = input("Enter the company name to search (0 for menu): "
                    ).strip()

                    if search_term == "0":
                        break

                    if search_term == "":
                        print("Search term cannot be empty.")
                        continue

                    companies = search_companies(connection, search_term)

                    if not companies:
                        print("No companies found.")
                        continue

                    for company in companies:
                        print(company)

        elif choice == "6":
            companies = get_companies(connection)

            if not companies:
                print("There are no companies. Add a company first.")
                continue

            for company in companies:
                print(company)

            valid_ids = []

            for company in companies:
                valid_ids.append(str(company[0]))

            while True:
                company_id = input(
                    "Select the company ID (0 to return to main menu): "
                ).strip()

                if company_id == "0":
                    break

                if company_id not in valid_ids:
                    print("There is no company with this ID.")
                    continue

                while True:
                    position = input(
                        "Enter the position (0 to go back): "
                    ).strip()

                    if position == "0":
                        break

                    if position == "":
                        print("Position cannot be empty.")
                        continue

                    statuses = (
                        "saved",
                        "applied",
                        "interview",
                        "offer",
                        "rejected",
                        "withdrawn",
                    )

                    while True:
                        for index, status in enumerate(statuses, start=1):
                            print(f"{index}. {status}")

                        status_choice = input(
                            "Select application status (0 to go back): "
                        ).strip()

                        if status_choice == "0":
                            break

                        try:
                            status_index = int(status_choice)
                        except ValueError:
                            print("Status selection must be a number.")
                            continue

                        if status_index < 1 or status_index > len(statuses):
                            print("Invalid status selection.")
                            continue

                        selected_status = statuses[status_index - 1]
                        applied_at = date.today().isoformat()

                        add_application(
                            connection,
                            int(company_id),
                            position,
                            selected_status,
                            applied_at,
                        )

                        print("Application added.")
                        break

                    if status_choice == "0":
                        continue

                    break

                if position == "0":
                    continue

                break
        

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


finally:
    connection.close()