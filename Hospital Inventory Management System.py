import os
import datetime


def login():
    Authorized_Users = {
        'admin1': '123abc',
        'admin2': 'helloworld',
        'admin3': 'apustudy',
        'admin4': 'python3'}
    attempts = 0
    max_login_attempts = 3
    while attempts < max_login_attempts:
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        if username in Authorized_Users and Authorized_Users[username] == password:
            print("Login successful!")
            return True
        else:
            attempts += 1
            print("Invalid credentials! Please try again.")
            print("Remaining Attempts:", max_login_attempts - attempts)
    print("You have been terminated from the system after 3 failed attempts.")
    return False


def main():
    print("Welcome to the Inventory Management System for PPE")
    if not login():
        print("Exiting the program")
        return

    initialize_inventory()
    while True:
        print("\nMenu:\n1. Manage Suppliers\n2. Update Inventory\n"
              "3. Manage Hospitals\n4. Item Inventory Tracking\n"
              "5. Search Distributions\n6. Generate Reports\n"
              "7. Exit")
        choice = input("Enter choice (number): ")
        if choice == '1':
            manage_supplier()
        elif choice == '2':
            update_inventory_menu()
        elif choice == '3':
            manage_hospital()
        elif choice == '4':
            track_inventory()
        elif choice == '5':
            search_distributions()
        elif choice == '6':
            generate_reports()
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again")


def initialize_inventory():
    ppe_items = {
        'HC': 'Head Cover',
        'FS': 'Face Shield',
        'MS': 'Mask',
        'GL': 'Gloves',
        'GW': 'Gown',
        'SC': 'Shoe Covers'}
    initial_quantity = 100
    try:
        with open("ppe.txt", "r"):
            print("Inventory already initialized.")
    except FileNotFoundError:
        print("Creating inventory....")
        with open("ppe.txt", "w") as file:
            for code, name in ppe_items.items():
                supplier_code = input(f"Enter Supplier Code for {name} ({code}): ")
                file.write(f"{code},{name},{supplier_code},{initial_quantity}\n")
        print("Inventory Initialization Complete.")


def display_total_quantity():
    with open("ppe.txt", "r") as file:
        items = []
        for line in file:
            item_code, item_name, supplier_code, quantity = line.strip().split(",")
            items.append((item_code, int(quantity)))
        items.sort()

        for item_code, quantity in items:
            print(f"{item_code}: {quantity}")


def display_low_stock_items():
    with open("ppe.txt", "r") as file:
        print("Items with stock less than 25 boxes:")
        for line in file:
            item_code, item_name, supplier_code, quantity = line.strip().split(",")
            if int(quantity) < 25:
                print(f"{item_code}: {quantity}")


def generate_suppliers_report():
    try:
        with open("suppliers.txt", "r") as file:
            print("List of Suppliers with their PPE Equipment supplied:")
            for line in file:
                supplier_code, supplier_name = line.strip().split(",")
                print(f"Supplier Code: {supplier_code}, Name: {supplier_name}")

    except FileNotFoundError:
        print("The file 'suppliers.txt' does not exist.")


def generate_hospitals_report():
    try:
        distribution_summary = {}
        with open("distribution.txt", "r") as file:
            for line in file:
                item_code, hospital_code, quantity = line.strip().split(",")
                quantity = int(quantity)
                if hospital_code in distribution_summary:
                    distribution_summary[hospital_code] += quantity
                else:
                    distribution_summary[hospital_code] = quantity

        print("List of Hospitals with quantity of distributed items:")
        for hospital_code, total_quantity in distribution_summary.items():
            print(f"Hospital Code: {hospital_code}, Total Quantity Distributed: {total_quantity}")

    except FileNotFoundError:
        print("The file 'distribution.txt' does not exist.")


def generate_transaction_report():
    try:
        transactions = []
        with open("distribution.txt", "r") as file:
            for line in file:
                item_code, hospital_code, quantity = line.strip().split(",")
                quantity = int(quantity)
                transactions.append((item_code, hospital_code, quantity))

        print("Overall Transaction Report:")
        for item_code, hospital_code, quantity in transactions:
            print(f"Item Code: {item_code}, Hospital Code: {hospital_code}, Quantity: {quantity}")

    except FileNotFoundError:
        print("The file 'distribution.txt' does not exist.")


def generate_reports():
    print("Generate report:")
    print("1. Hospitals report")
    print("2. Suppliers report")
    print("3. Overall transaction report")
    print("4. Return back to main menu")
    choice = input("Enter your choice: ")
    if choice == "1":
        generate_hospitals_report()
    elif choice == "2":
        generate_suppliers_report()
    elif choice == "3":
        generate_transaction_report()
    elif choice == '4':
        return
    else:
        print("Invalid choice. Please select a valid option.")


def manage_supplier():
    suppliers = {}
    # Load existing suppliers
    try:
        with open('suppliers.txt', 'r') as file:
            for line in file:
                code, name = line.strip().split(',')
                suppliers[code] = name
    except FileNotFoundError:
        pass  # If the file does not exist, start with an empty dictionary

    while True:
        print("\nManage Suppliers:")
        print("1. Add Supplier")
        print("2. View Suppliers")
        print("3. Return to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            supplier_code = input("Enter supplier code: ")
            if supplier_code in suppliers:
                print("Supplier code already exists. Please enter a unique code.")
                continue
            supplier_name = input("Enter supplier name: ")
            suppliers[supplier_code] = supplier_name
            # Save the updated suppliers list to file
            with open('suppliers.txt', 'w') as file:
                for code, name in suppliers.items():
                    file.write(f"{code},{name}\n")
            print("Supplier information saved.")
        elif choice == '2':
            print("\nExisting Suppliers:")
            for code, name in suppliers.items():
                print(f"Code: {code}, Name: {name}")
        elif choice == '3':
            print("Returning to main menu.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


def update_inventory(item_code, quantity, operation):
    inventory = {}
    # Read current inventory from ppe.txt
    with open('ppe.txt', 'r') as file:
        for line in file:
            code, name, supplier_code, qty = line.strip().split(',')
            inventory[code] = int(qty)

    if item_code not in inventory:
        print("Item code not found in inventory.")
        return False

    # Perform the required operation (receive or distribute)
    if operation == 'receive':
        inventory[item_code] += quantity
    elif operation == 'distribute':
        if inventory[item_code] >= quantity:
            inventory[item_code] -= quantity
        else:
            print("Insufficient quantity in stock.")
            return False

    # Write the updated inventory back to ppe.txt
    with open('ppe.txt', 'w') as file:
        for code, qty in inventory.items():
            file.write(f"{code},{inventory[code]},{qty}\n")  # Use the actual supplier name if available
    print("Inventory updated.")
    return True


def receive_from_supplier():
    item_code = input("Enter item code: ")
    try:
        quantity = int(input("Enter quantity received: "))
        if quantity <= 0:
            raise ValueError("Quantity must be a positive number.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    if update_inventory(item_code, quantity, 'receive'):
        print("Received from supplier recorded.")
    else:
        print("Failed to record received items due to inventory issues.")


def distribute_to_hospital():
    item_code = input("Enter item code: ")
    try:
        quantity = int(input("Enter quantity to distribute: "))
        if quantity <= 0:
            raise ValueError("Quantity must be a positive number.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    hospital_code = input("Enter hospital code: ")

    if update_inventory(item_code, quantity, 'distribute'):
        with open('distribution.txt', 'a') as file:
            file.write(f"{item_code},{hospital_code},{quantity}\n")
        print("Distribution recorded.")
    else:
        print("Distribution failed due to inventory issues.")


def update_inventory_menu():
    print("Update Inventory:")
    print("1. Receive from Supplier")
    print("2. Distribute to Hospital")
    choice = input("Enter your choice: ")

    if choice == '1':
        receive_from_supplier()
    elif choice == '2':
        distribute_to_hospital()
    else:
        print("Invalid choice. Returning to main menu.")


def manage_hospital():
    hospitals = {}
    # Load existing hospitals
    try:
        with open('hospitals.txt', 'r') as file:
            for line in file:
                code, name = line.strip().split(',')
                hospitals[code] = name
    except FileNotFoundError:
        pass  # If the file does not exist, start with an empty dictionary

    while True:
        print("\nManage Hospitals:")
        print("1. Add Hospital")
        print("2. View Hospitals")
        print("3. Return to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            hospital_code = input("Enter hospital code: ")
            if hospital_code in hospitals:
                print("Hospital code already exists. Please enter a unique code.")
                continue
            hospital_name = input("Enter hospital name: ")
            hospitals[hospital_code] = hospital_name
            # Save the updated hospitals list to file
            with open('hospitals.txt', 'w') as file:
                for code, name in hospitals.items():
                    file.write(f"{code},{name}\n")
            print("Hospital information saved.")
        elif choice == '2':
            print("\nExisting Hospitals:")
            for code, name in hospitals.items():
                print(f"Code: {code}, Name: {name}")
        elif choice == '3':
            print("Returning to main menu.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


def track_inventory():
    print("Item Inventory Tracking:")
    print("1. Total available quantity of all items sorted by item code")
    print("2. Items with stock less than 25 boxes")
    try:
        choice = int(input("Enter your choice (1/2): "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    if choice == 1:
        display_total_quantity()
    elif choice == 2:
        display_low_stock_items()
    else:
        print("Invalid choice. Returning to main menu.")


def search_distributions():
    item_code = input("Enter item code to search: ").strip()

    try:
        with open("distribution.txt", "r") as file:
            distribution_summary = {}

            for line in file:
                code, hospital_code, quantity = line.strip().split(",")
                if code == item_code:
                    quantity = int(quantity)
                    if hospital_code in distribution_summary:
                        distribution_summary[hospital_code] += quantity
                    else:
                        distribution_summary[hospital_code] = quantity

            if distribution_summary:
                print(f"Distribution list for Item {item_code}:")
                for hospital_code, quantity in distribution_summary.items():
                    print(f"Hospital Code: {hospital_code}, Quantity: {quantity}")
            else:
                print(f"No distributions found for Item {item_code}.")

    except FileNotFoundError:
        print("The file 'distribution.txt' does not exist.")


if _name_ == "_main_":
    main()