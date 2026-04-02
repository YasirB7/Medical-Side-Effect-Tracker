import csv
import os
from datetime import datetime

FILENAME = "side_effects.csv"


def initialize_file():
    """Create the CSV file with headers if it does not exist or is empty."""
    if not os.path.exists(FILENAME) or os.path.getsize(FILENAME) == 0:
        with open(FILENAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Medication", "Side Effect", "Severity", "Date"])


def add_entry():
    """Add a new side effect entry to the CSV file."""
    medication = input("Enter medication name: ").strip()
    side_effect = input("Enter side effect: ").strip()

    while True:
        severity = input("Enter severity (1-5): ").strip()
        if severity.isdigit() and 1 <= int(severity) <= 5:
            severity = int(severity)
            break
        print("Invalid input. Please enter a number from 1 to 5.")

    date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if date_input == "":
        date_input = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Using today's date instead.")
            date_input = datetime.today().strftime("%Y-%m-%d")

    with open(FILENAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([medication, side_effect, severity, date_input])

    print("Entry added successfully.\n")


def view_entries():
    """Display all logged side effect entries."""
    with open(FILENAME, mode="r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) <= 1:
        print("No entries found.\n")
        return

    print("\nLogged Side Effects:")
    print("-" * 60)
    for row in rows[1:]:
        print(f"Medication: {row[0]}")
        print(f"Side Effect: {row[1]}")
        print(f"Severity: {row[2]}")
        print(f"Date: {row[3]}")
        print("-" * 60)
    print()


def show_summary():
    """Show a summary of side effects and average severity."""
    with open(FILENAME, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        print("No entries available for summary.\n")
        return

    side_effect_counts = {}
    medication_severity = {}

    for row in rows:
        side_effect = row["Side Effect"]
        medication = row["Medication"]
        severity = int(row["Severity"])

        side_effect_counts[side_effect] = side_effect_counts.get(side_effect, 0) + 1

        if medication not in medication_severity:
            medication_severity[medication] = []
        medication_severity[medication].append(severity)

    print("\nSummary Report")
    print("-" * 60)

    print("Most Common Side Effects:")
    for effect, count in side_effect_counts.items():
        print(f"{effect}: {count}")

    print("\nAverage Severity by Medication:")
    for medication, severities in medication_severity.items():
        average = sum(severities) / len(severities)
        print(f"{medication}: {average:.2f}")

    print()


def main():
    """Main menu loop."""
    initialize_file()

    while True:
        print("Medical Side Effect Tracker")
        print("1. Add Entry")
        print("2. View Entries")
        print("3. Show Summary")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_entry()
        elif choice == "2":
            view_entries()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()