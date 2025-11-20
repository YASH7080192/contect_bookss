# ------------------------------------------------------------
# Name: Yashvant Giri
# Date: 20-11-2025
# Project: Contact Book Management System (CSV + JSON)
# ------------------------------------------------------------

import csv
import json
from datetime import datetime

CSV_FILE = "contacts.csv"
JSON_FILE = "contacts.json"
ERROR_LOG = "error_log.txt"


# -------------------------------------------
# BONUS: Log Errors
# -------------------------------------------
def log_error(message, operation):
    with open(ERROR_LOG, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] ERROR in {operation}: {message}\n")


# -------------------------------------------
# TASK 1: Welcome Message
# -------------------------------------------
print("\n===== CONTACT BOOK MANAGEMENT SYSTEM =====")
print("This tool lets you store, view, search, update, and delete contacts.\n")


# -------------------------------------------
# TASK 2: Add & Save Contact (CSV)
# -------------------------------------------
def add_contact():
    try:
        name = input("Enter Name: ")
        phone = input("Enter Phone Number: ")
        email = input("Enter Email: ")

        contact = {"name": name, "phone": phone, "email": email}

        # Write to CSV
        try:
            file_exists = False
            try:
                open(CSV_FILE, "r")
                file_exists = True
            except:
                pass

            with open(CSV_FILE, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["name", "phone", "email"])
                if not file_exists:
                    writer.writeheader()
                writer.writerow(contact)

            print("✔ Contact Saved Successfully!\n")

        except Exception as e:
            log_error(str(e), "Adding Contact")
            print("❌ Error saving contact!")

    except Exception as e:
        log_error(str(e), "Input")
        print("❌ Invalid input!")


# -------------------------------------------
# TASK 3: Read & Display Contacts
# -------------------------------------------
def view_contacts():
    try:
        with open(CSV_FILE, "r") as f:
            reader = csv.DictReader(f)
            contacts = list(reader)

            if not contacts:
                print("No contacts found!\n")
                return

            print("\n----- SAVED CONTACTS -----")
            print("Name\t\tPhone\t\tEmail")
            print("--------------------------------------------")

            for c in contacts:
                print(f"{c['name']}\t\t{c['phone']}\t\t{c['email']}")
            print()

    except FileNotFoundError:
        log_error("CSV file missing", "Display Contacts")
        print("❌ No contacts found! (CSV missing)\n")

    except Exception as e:
        log_error(str(e), "Display Contacts")
        print("❌ Error reading contacts!\n")


# -------------------------------------------
# TASK 4: SEARCH / UPDATE / DELETE
# -------------------------------------------
def load_csv():
    try:
        with open(CSV_FILE, "r") as f:
            return list(csv.DictReader(f))
    except:
        return []


def save_csv(data):
    try:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "phone", "email"])
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        log_error(str(e), "Save CSV")


# Search
def search_contact():
    name = input("Enter name to search: ").lower()
    contacts = load_csv()
    found = [c for c in contacts if c["name"].lower() == name]

    if found:
        print("\n✔ Contact Found:")
        for c in found:
            print(f"Name: {c['name']}\nPhone: {c['phone']}\nEmail: {c['email']}\n")
    else:
        print("❌ Contact not found!\n")


# Update
def update_contact():
    name = input("Enter name to update: ").lower()
    contacts = load_csv()
    updated = False

    for c in contacts:
        if c["name"].lower() == name:
            print("What do you want to update?")
            print("1. Phone Number")
            print("2. Email Address")
            choice = input("Enter choice: ")

            if choice == "1":
                c["phone"] = input("Enter new phone: ")
            elif choice == "2":
                c["email"] = input("Enter new email: ")

            updated = True
            break

    if updated:
        save_csv(contacts)
        print("✔ Contact Updated!\n")
    else:
        print("❌ Contact not found!\n")


# Delete
def delete_contact():
    name = input("Enter name to delete: ").lower()
    contacts = load_csv()
    new_contacts = [c for c in contacts if c["name"].lower() != name]

    if len(new_contacts) != len(contacts):
        save_csv(new_contacts)
        print("✔ Contact Deleted!\n")
    else:
        print("❌ Contact not found!\n")


# -------------------------------------------
# TASK 5: CSV → JSON & JSON → Display
# -------------------------------------------
def export_json():
    try:
        contacts = load_csv()
        with open(JSON_FILE, "w") as f:
            json.dump(contacts, f, indent=4)
        print("✔ Exported to JSON successfully!\n")
    except Exception as e:
        log_error(str(e), "Export JSON")
        print("❌ Error exporting JSON!\n")


def load_json():
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)

        print("\n----- CONTACTS FROM JSON -----")
        for c in data:
            print(f"{c['name']} - {c['phone']} - {c['email']}")
        print()

    except Exception as e:
        log_error(str(e), "Load JSON")
        print("❌ Error loading JSON!\n")


# -------------------------------------------
# MAIN MENU
# -------------------------------------------
def menu():
    while True:
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Export Contacts to JSON")
        print("7. Load Contacts from JSON")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            export_json()
        elif choice == "7":
            load_json()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.\n")


menu()
