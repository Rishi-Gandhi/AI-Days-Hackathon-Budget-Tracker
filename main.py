import csv
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from openai import OpenAI
import json

client = OpenAI(api_key="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")

DATA_FILE = "budget_data.csv"
budget_limit = 0.0


def init_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Amount", "Date"])

def set_budget():
    global budget_limit
    budget_limit = float(input("Enter your total budget: "))
    print(f"✅ Budget set to ${budget_limit:.2f}\n")

def add_expense():
    global budget_limit
    categories = ["Food", "Entertainment", "Shopping", "Transportation", "Random"]

    print("\nChoose a category:")
    for i, c in enumerate(categories, 1):
        print(f"{i}. {c}")
    choice = int(input("Enter number: "))
    category = categories[choice - 1]

    amount = float(input("Enter expense amount: "))
    date = input("Enter date (YYYY-MM-DD): ")

    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([category, amount, date])
    print("✅ Expense added successfully!\n")

    total_expenses = get_total_expenses()
    remaining = budget_limit - total_expenses

    # Budget warnings
    if total_expenses >= budget_limit:
        print(f"⚠️ You went over your budget by ${total_expenses - budget_limit:.2f}!\n")
    elif total_expenses >= 0.8 * budget_limit:
        print("⚠️ You’ve reached 80% of your budget! Be careful with spending.\n")

    print(f"💵 Remaining budget: ${remaining:.2f}\n")

    give_ai_feedback()

    see_chart = input("Would you like to see your spending chart? (yes/no): ").strip().lower()
    if see_chart == "yes":
        show_spending_chart()

def get_total_expenses():
    total = 0.0
    with open(DATA_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            total += float(row["Amount"])
    return total

def show_spending_chart():
    category_totals = defaultdict(float)
    with open(DATA_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            category_totals[row["Category"]] += float(row["Amount"])

    if not category_totals:
        print("No expenses yet to display!")
        return

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140,
            colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0"])
    plt.title("Spending Breakdown by Category")
    plt.show()

def give_ai_feedback():
    global budget_limit
    data = []
    with open(DATA_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    prompt = f"""
    I have a budget of ${budget_limit:.2f}.
    Here are my expenses so far:
    {json.dumps(data, indent=2)}

    Based on the budget I have and the money I spent on the categories so far,
    give me some feedback/advice. Make it concise and actionable. Also give advice that is relevant to the categories I have spent the most on.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        print("\n🧠 AI Feedback:")
        print(response.choices[0].message.content)
        print()
    except Exception as e:
        print(f"Error generating AI feedback: {e}")

def view_summary():
    total_expenses = get_total_expenses()
    remaining = budget_limit - total_expenses

    print("\n----- 💰 Expense Summary -----")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Remaining Budget: ${remaining:.2f}")
    print(f"Budget Limit: ${budget_limit:.2f}")
    print("-----------------------------\n")

def main():
    init_file()
    while True:
        print("===== Smart Expense Tracker =====")
        print("1. Set Budget")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            set_budget()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_summary()
        elif choice == "4":
            print("👋 Goodbye! Stay smart with your spending.")
            break
        else:
            print("❌ Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
