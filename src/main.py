from datetime import date
from datetime import datetime

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
from database import get_applications
from database import update_application
from database import delete_application
from database import create_application_status_history_table
from database import add_application_status_history
from database import get_application_status_history

def show_menu() -> None:
    print("\n1. Add company")
    print("2. List companies")
    print("3. Delete company")
    print("4. Update company")
    print("5. Search company")
    print("6. Add application")
    print("7. List applications")
    print("8. Update application")
    print("9. Delete application")
    print("10. View application status history")
    print("0. Exit")


connection = create_connection()


try:
    create_companies_table(connection)
    create_applications_table(connection)
    create_application_status_history_table(connection)

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
                        created_at = datetime.now().isoformat(timespec="seconds")

                        add_application(
                            connection,
                            int(company_id),
                            position,
                            selected_status,
                            created_at,
                        )

                        print("Application added.")
                        break

                    if status_choice == "0":
                        continue

                    break

                if position == "0":
                    continue

                break
                
        elif choice == "7":
            applications = get_applications(connection)

            if not applications:
                print("There are no applications.")
                continue

            for application in applications:
                history = get_application_status_history(
                    connection,
                    application[0],
                )

                if len(history) > 1:
                    last_updated = history[-1][2]
                else:
                    last_updated = application[4]

                print(
                    f"ID: {application[0]} | "
                    f"Company: {application[1]} | "
                    f"Position: {application[2]} | "
                    f"Status: {application[3]} | "
                    f"Last updated: {last_updated}"
                )
        
        elif choice == "8":
            applications = get_applications(connection)

            if not applications:
                print("There are no applications.")
                continue

            for application in applications:
                print(
                    f"ID: {application[0]} | "
                    f"Company: {application[1]} | "
                    f"Position: {application[2]} | "
                    f"Status: {application[3]} | "
                    f"Applied at: {application[4]}"
                )

            valid_ids = []

            for application in applications:
                valid_ids.append(str(application[0]))            

            while True:
                application_id = input(
                    "Select the application ID (0 to return to main menu): "
                ).strip()

                if application_id == "0":
                    break

                if application_id not in valid_ids:
                    print("There is no application with this ID.")
                    continue

                selected_application = None

                for application in applications:
                    if str(application[0]) == application_id:
                        selected_application = application
                        break    

                while True:
                    new_position = input(
                        "Enter the new position (0 to go back): "
                    ).strip()

                    if new_position == "0":
                        break

                    if new_position == "":
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
                            "Select the new status (0 to go back): "
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

                        update_application(
                            connection,
                            int(application_id),
                            new_position,
                            selected_status,
                        )

                        if selected_status != selected_application[3]:
                            changed_at = datetime.now().isoformat(timespec="seconds")
                            add_application_status_history(
                                connection,
                                int(application_id),
                                selected_status,
                                changed_at,
                            )        

                        print(
                            f"Application number {application_id} is updated."
                        )
                        break

                    if status_choice == "0":
                        continue

                    break

                if new_position == "0":
                    continue

                break
            
        elif choice == "9":
            applications = get_applications(connection)

            if not applications:
                print("There are no applications.")
                continue

            for application in applications:
                print(
                    f"ID: {application[0]} | "
                    f"Company: {application[1]} | "
                    f"Position: {application[2]} | "
                    f"Status: {application[3]} | "
                    f"Applied at: {application[4]}"
                )

            valid_ids = []

            for application in applications:
                valid_ids.append(str(application[0]))

            while True:
                application_id = input(
                    "Select the application ID to delete "
                    "(0 to return to main menu): "
                ).strip()

                if application_id == "0":
                    break

                if application_id not in valid_ids:
                    print("There is no application with this ID.")
                    continue

                delete_application(connection, int(application_id))
                print(f"Application number {application_id} is deleted.")
                break

        elif choice == "10":
            applications = get_applications(connection)

            if not applications:
                print("There are no applications.")
                continue

            for application in applications:
                print(
                    f"ID: {application[0]} | "
                    f"Company: {application[1]} | "
                    f"Position: {application[2]} | "
                    f"Status: {application[3]}"
                )

            valid_ids = []

            for application in applications:
                valid_ids.append(str(application[0]))

            application_id = input(
                "Select the application ID "
                "(0 to return to main menu): "
            ).strip()

            if application_id == "0":
                continue

            if application_id not in valid_ids:
                print("There is no application with this ID.")
                continue

            history = get_application_status_history(
                connection,
                int(application_id),
            )

            if not history:
                print("There is no status history for this application.")
                continue

            for history_record in history:
                print(
                    f"Status: {history_record[1]} | "
                    f"Changed at: {history_record[2]}"
                )
        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


finally:
    connection.close()