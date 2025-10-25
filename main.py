import csv
import os
import matplotlib.pyplot as plt
from collections import defaultdict

# File to store transactions
DATA_FILE = "budget_data.csv"

# Global budget limit
budget_limit = 0.0

# Initialize CSV file if it doesn't exist
def init_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Category", "Amount", "Date"])

# Add income
def add_income():
    category = input("Enter income category (e.g., Job, Gift): ")
    amount = float(input("Enter income amount: "))
    date = input("Enter date (MM-DD-YYYY): ")

    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Income", category, amount, date])
    print("✅ Income added successfully!\n")

# Add expense
def add_expense():
    global budget_limit
    category = input("Enter expense category (e.g., Food, Rent): ")
    amount = float(input("Enter expense amount: "))
    date = input("Enter date (MM-DD-YYYY): ")

    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Expense", category, amount, date])
    print("✅ Expense added successfully!\n")

    # Check if expenses exceed budget
    if budget_limit > 0:
        total_expenses = get_total("Expense")
        if total_expenses > budget_limit:
            print("⚠️ ALERT: You’ve exceeded your monthly budget limit!\n")

# Calculate total income or expenses
def get_total(type_name):
    total = 0.0
    with open(DATA_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Type"] == type_name:
                total += float(row["Amount"])
    return total

# View summary
def view_summary():
    total_income = get_total("Income")
    total_expenses = get_total("Expense")
    balance = total_income - total_expenses

    print("\n----- 💰 Budget Summary -----")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Remaining Balance: ${balance:.2f}")
    if budget_limit > 0:
        print(f"Budget Limit: ${budget_limit:.2f}")
    print("-----------------------------\n")

# Set budget limit
def set_budget():
    global budget_limit
    budget_limit = float(input("Enter your monthly budget limit: "))
    print(f"✅ Budget limit set to ${budget_limit:.2f}\n")

def show_spending_chart():
    # Dictionary to store total expenses per category
    category_totals = defaultdict(float)

    with open(DATA_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Type"] == "Expense":
                category_totals[row["Category"]] += float(row["Amount"])

    if not category_totals:
        print("No expenses to display yet!")
        return

    # Prepare data for the chart
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    # Create pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140,colors=["#ff9999","#66b3ff","#99ff99","#f5e905"])
    plt.title("Spending Breakdown by Category")
    plt.show()

# Main menu
def main():
    init_file()
    while True:
        print("===== Student Budget Buddy =====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. Set Budget Limit")
        print("5. Exit")
        print("6. Show Spending Chart")


        choice = input("Choose an option: ")

        if choice == "1":
            add_income()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_summary()
        elif choice == "4":
            set_budget()
        elif choice == "5":
            print("👋 Exiting Budget Buddy. Goodbye!")
            break
        elif choice == "6":
            show_spending_chart()
        else:
            print("❌ Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
