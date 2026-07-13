from database import add_company, create_companies_table, create_connection, get_companies,delete_company


def show_menu() -> None:
    print("\n1. Add company")
    print("2. List companies")
    print("3. Delete company")
    print("0. Exit")


connection = create_connection()


try:
    create_companies_table(connection)

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            company_name = input("Company name: ").strip()
            company_country = input("Company country: ").strip()

            if company_name == "" or company_country == "":
                print("Company name and country cannot be empty.")
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
                company_id = input("Enter the ID of the company you want to delete,(0 to cancel) ").strip()
                
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
                    
        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


finally:
    connection.close()