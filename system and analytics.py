import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Developer comment: This is the final version of the project, if anyone edits this make sure to not change anything functional - F
# Note: The program will auto-create 'tickets2024.csv' with some sample data if the file does not exist or is empty, for initial testing.
CSV_FILE = "tickets2024.csv"
FIELDNAMES = ["Ticket ID", "Event Name", "Customer Name", "Purchase Date", "Ticket Price", "Quantity", "Total Cost"]

def seed_sample_data():
    """Create a CSV file with sample ticket data if it doesn't exist or is empty."""
    sample_Rows = [
        {"Ticket ID": "1", "Event Name": "Concert A", "Customer Name": "Ahmed Ali", "Purchase Date": "2024-01-13", "Ticket Price": "40", "Quantity": "2", "Total Cost": str(40 * 2)},
        {"Ticket ID": "2", "Event Name": "Concert B", "Customer Name": "Sara Saad", "Purchase Date": "2024-01-13", "Ticket Price": "85", "Quantity": "1", "Total Cost": str(85 * 1)},
        {"Ticket ID": "3", "Event Name": "Concert A", "Customer Name": "Ali Fahad", "Purchase Date": "2024-01-12", "Ticket Price": "10", "Quantity": "1", "Total Cost": str(10 * 1)},
        {"Ticket ID": "4", "Event Name": "Conference X", "Customer Name": "Basmah Emad", "Purchase Date": "2024-01-12", "Ticket Price": "100", "Quantity": "3", "Total Cost": str(100 * 3)}
    ]
    # Only seed if file is missing or empty
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        with open(CSV_FILE, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for row in sample_Rows:
                writer.writerow(row)

def login():
    """Prompt for username/password and verify credentials."""
    username = "admin"
    password = "admin123"
    attempts = 3
    while attempts > 0:
        log_User = input("Username: ").strip()
        log_Pass = input("Password: ").strip()
        if log_User == username and log_Pass == password:
            print("You have successfully logged in!\n")
            return True
        else:
            attempts -= 1
            if attempts > 0:
                print(f"Invalid credentials. Please try again. ({attempts} attempts remaining)\n")
    print("Too many failed login attempts. Access denied.")
    return False

def ticket_Dict():
    """Read all ticket records from the CSV file and return as a list of dictionaries."""
    all_Tickets = []
    if not os.path.exists(CSV_FILE):
        return all_Tickets
    with open(CSV_FILE, mode='r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_Tickets.append(row)
    return all_Tickets

def new_Ticket():
    """Add a new ticket sale to the system (and CSV file) with user-provided details."""
    print("==== Add New Ticket ====")
    # Ensure CSV file exists and has header
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
    # Ticket ID (must be unique and numeric)
    while True:
        ticket_ID = input("Please enter Ticket ID (numeric): ").strip()
        if ticket_ID == "":
            print("Error detected: Ticket ID cannot be empty. Please try again.")
            continue
        if not ticket_ID.isdigit():
            print("Error detected: Ticket ID must be a number. Please try again.")
            continue
        # Check if ID already exists
        if any(t.get("Ticket ID") == ticket_ID for t in ticket_Dict()):
            print("This Ticket ID already exists. Please enter a unique Ticket ID.")
            continue
        break
    # Event Name (must not be empty)
    while True:
        eventName = input("Enter Event Name: ").strip()
        if eventName == "":
            print("Error detected: Event Name cannot be empty. Please try again.")
            continue
        break
    # Customer Name (must not be empty)
    while True:
        customer_Name = input("Enter Customer Name: ").strip()
        if customer_Name == "":
            print("Error detected: Customer Name cannot be empty. Please try again.")
            continue
        break
    # Purchase Date in YYYY-MM-DD format
    while True:
        purchase_Date = input("Enter Purchase Date (YYYY-MM-DD): ").strip()
        if purchase_Date == "":
            print("Error detected: Purchase Date cannot be empty. Please try again.")
            continue
        try:
            datetime.strptime(purchase_Date, "%Y-%m-%d")  # validate format
        except ValueError:
            print("Error detected: Invalid date format. Please enter date as YYYY-MM-DD.")
            continue
        break
    # Ticket Price (must be numeric but can be either float or int)
    while True:
        priceInpt = input("Enter Ticket Price: ").strip()
        if priceInpt == "":
            print("Error detected: Ticket Price cannot be empty. Please try again.")
            continue
        try:
            priceVal = float(priceInpt)
        except ValueError:
            print("Error detected: Ticket Price must be a number. Please try again.")
            continue
        if priceVal < 0:
            print("Error detected: Ticket Price cannot be negative. Please enter a valid price.")
            continue
        break
    # Quantity (numeric value, must be an integer)
    while True:
        qtyInpt = input("Enter Quantity: ").strip()
        if qtyInpt == "":
            print("Error detected: Quantity cannot be empty. Please try again.")
            continue
        if not qtyInpt.isdigit():
            print("Error detected: Quantity must be a positive integer. Please try again.")
            continue
        qtyVal = int(qtyInpt)
        if qtyVal <= 0:
            print("Quantity must be at least 1. Please try again.")
            continue
        break
    # Calculate total cost (price * quantity)
    totalCost_val = round(priceVal * qtyVal, 2)
    # Format price and total cost for storage/output
    priceStr = str(int(priceVal)) if priceVal.is_integer() else f"{priceVal:.2f}"
    totalCost_Str = str(int(totalCost_val)) if float(totalCost_val).is_integer() else f"{totalCost_val:.2f}"
    # Create ticket record
    ticket_Record = {
        "Ticket ID": ticket_ID,
        "Event Name": eventName,
        "Customer Name": customer_Name,
        "Purchase Date": purchase_Date,
        "Ticket Price": priceStr,
        "Quantity": str(qtyVal),
        "Total Cost": totalCost_Str
    }
    # Write the new record to CSV
    try:
        with open(CSV_FILE, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            # Write header if file was empty/new
            if os.path.getsize(CSV_FILE) == 0:
                writer.writeheader()
            writer.writerow(ticket_Record)
        print("Ticket added successfully!")
    except Exception as e:
        print(f"Error: Could not write to file ({e}).")

def view_All():
    """Display all tickets in the system with their details."""
    print("==== All Ticket Sales ====")
    tickets = ticket_Dict()
    if not tickets:
        print("No tickets available.")
    else:
        for t in tickets:
            # Extract fields with safe defaults if missing
            tID = t.get("Ticket ID", "")
            event = t.get("Event Name", "")
            customer = t.get("Customer Name", "")
            date = t.get("Purchase Date", "")
            price = t.get("Ticket Price", "")
            qty = t.get("Quantity", "")
            total = t.get("Total Cost", "")
            print(f"Ticket ID: {tID}, Event: {event}, Customer: {customer}, Date: {date}, Price: {price}, Quantity: {qty}, Total: {total}")
    print("")  # blank line for spacing

def ticket_Search():
    """Search for a ticket by Ticket ID and display its details if found."""
    print("==== Search Ticket by ID ====")
    tickets = ticket_Dict()
    if not tickets:
        print("No tickets available to search.")
        return
    search_ID = input("Enter Ticket ID to search: ").strip()
    if search_ID == "":
        print("Error detected: Ticket ID cannot be empty.")
        return
    found = False
    for t in tickets:
        if t.get("Ticket ID") == search_ID:
            found = True
            print("Ticket found:")
            print(f"Ticket ID: {t.get('Ticket ID')}")
            print(f"Event Name: {t.get('Event Name')}")
            print(f"Customer Name: {t.get('Customer Name')}")
            print(f"Purchase Date: {t.get('Purchase Date')}")
            print(f"Ticket Price: {t.get('Ticket Price')}")
            print(f"Quantity: {t.get('Quantity')}")
            print(f"Total Cost: {t.get('Total Cost')}\n")
            break
    if not found:
        print("Sorry, but the ticket you are looking for does not exist.\n")

def generate_Reports():
    """Show a submenu for reports and generate selected report with visualization."""
    while True:
        print("==== Generate Reports ====")
        print("1: Total Sales by Event")
        print("2: Sales Over Time")
        print("3: Sales Summary (Average, Max, Min)")
        print("B: Back to Main Menu")
        choice = input("Please select a report option: ").strip().upper()
        tickets = ticket_Dict()
        if choice == 'B':
            break  # return to main menu
        if not tickets:
            print("No data available to generate reports.")
            continue
        if choice == '1':
            # Report 1: Total sales by event (tickets sold per event) and revenue by event
            event_Sales = {}   # event -> total tickets sold
            event_Rev = {} # event -> total revenue
            for t in tickets:
                event = t.get("Event Name", "Unknown")
                try:
                    qty = int(float(t.get("Quantity", 0)))
                except:
                    qty = 0
                try:
                    revenue = float(t.get("Total Cost", 0.0))
                except:
                    revenue = 0.0
                event_Sales[event] = event_Sales.get(event, 0) + qty
                event_Rev[event] = event_Rev.get(event, 0.0) + revenue
            # Prepare data for charts
            events = list(event_Sales.keys())
            sales_Counts = [event_Sales[e] for e in events]
            revenues = [event_Rev[e] for e in events]
            # Bar chart: Tickets sold by event
            plt.figure(figsize=(6,4))
            plt.bar(events, sales_Counts, color='skyblue')
            plt.title("Tickets Sold by Event")
            plt.xlabel("Event")
            plt.ylabel("Tickets Sold")
            plt.tight_layout()
            plt.show()
            # Bar chart: Revenue by event
            plt.figure(figsize=(6,4))
            plt.bar(events, revenues, color='lightgreen')
            plt.title("Revenue by Event")
            plt.xlabel("Event")
            plt.ylabel("Total Revenue")
            plt.tight_layout()
            plt.show()
        elif choice == '2':
            # Report 2: Sales over time (line chart of tickets sold per date)
            date_Sales = {}  # date -> total tickets sold on that date
            for t in tickets:
                date = t.get("Purchase Date", "")
                if date == "":
                    continue
                try:
                    qty = int(float(t.get("Quantity", 0)))
                except:
                    qty = 0
                date_Sales[date] = date_Sales.get(date, 0) + qty
            if not date_Sales:
                print("No dates available for sales data.")
                continue
            # Sort dates chronologically
            dates = sorted(date_Sales.keys())
            salesBy_date = [date_Sales[d] for d in dates]
            # Line chart for sales over time
            plt.figure(figsize=(6,4))
            plt.plot(dates, salesBy_date, marker='o', linestyle='-')
            plt.title("Tickets Sold Over Time")
            plt.xlabel("Date")
            plt.ylabel("Tickets Sold")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        elif choice == '3':
            # Report 3: Summary statistics of sales (average, max, min tickets sold per day)
            date_Sales = {}
            for t in tickets:
                date = t.get("Purchase Date", "")
                if date == "":
                    continue
                try:
                    qty = int(float(t.get("Quantity", 0)))
                except:
                    qty = 0
                date_Sales[date] = date_Sales.get(date, 0) + qty
            if not date_Sales:
                print("No sales data to compute statistics.")
                continue
            daily_totals = list(date_Sales.values())
            avg_Sales = sum(daily_totals) / len(daily_totals)
            max_Sales = max(daily_totals)
            min_Sales = min(daily_totals)
            print(f"Average tickets sold per day: {avg_Sales:.2f}")
            print(f"Maximum tickets sold in a day: {max_Sales}")
            print(f"Minimum tickets sold in a day: {min_Sales}")
        else:
            print("{0} is not a valid option. Please select a valid report or select 'B' to go back.".format(choice))

def main_menu():
    """Displays the main menu."""
    while True:
        print("==== Ticket Manager ====")
        print("E: Enter New Ticket Details")
        print("V: View All Ticket Details")
        print("S: Search via Ticket ID")
        print("R: Produce Reports")
        print("Q: Quit/Log Out")
        choice = input("Please enter your choice: ").strip().upper()
        if choice == 'E':
            new_Ticket()
        elif choice == 'V':
            view_All()
        elif choice == 'S':
            ticket_Search()
        elif choice == 'R':
            generate_Reports()
        elif choice == 'Q':
            print("Thank you for using the ticket management system, see you soon!")
            break
        else:
            print("Error: {0} is not a valid choice. Please try again.\n".format(choice))

# This code runs the program
if __name__ == "__main__":
    seed_sample_data()     # Seed initial data if needed
    if login():            # Check for successful login
        main_menu()        # Show main menu if login was successful  
