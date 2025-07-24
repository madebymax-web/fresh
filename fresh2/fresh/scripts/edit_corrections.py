import json
import os

CORRECTIONS_FILE = "corrections.json"  # adjust path if needed

def load_corrections(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Invalid JSON file. Starting with empty corrections.")
    return {}

def save_corrections(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Corrections saved to {path}")

def display_corrections(corrections):
    if not corrections:
        print("No corrections found.")
        return
    print("\nCurrent Corrections:")
    for wrong, right in corrections.items():
        print(f"  '{wrong}' -> '{right}'")

def edit_mode(corrections):
    display_corrections(corrections)
    key = input("\nEnter the incorrect word to edit: ").strip()
    if key not in corrections:
        print("That entry doesn't exist.")
        return
    new_value = input(f"Replace '{key}' -> '{corrections[key]}' with: ").strip()
    if new_value:
        corrections[key] = new_value
        print("Entry updated.")

def add_mode(corrections):
    while True:
        wrong = input("\nMisheard word (or 'q' to quit): ").strip()
        if wrong.lower() == "q":
            break
        if wrong in corrections:
            print(f"'{wrong}' already maps to '{corrections[wrong]}'")
            continue
        right = input(f"Correct version of '{wrong}': ").strip()
        if right:
            corrections[wrong] = right
            print(f"Added: '{wrong}' -> '{right}'")

def main():
    corrections = load_corrections(CORRECTIONS_FILE)

    while True:
        print("\n--- Correction Dictionary Editor ---")
        print("1. Add new corrections")
        print("2. View existing corrections")
        print("3. Edit an existing correction")
        print("4. Save and exit")
        choice = input("Choose an option [1-4]: ").strip()

        if choice == "1":
            add_mode(corrections)
        elif choice == "2":
            display_corrections(corrections)
        elif choice == "3":
            edit_mode(corrections)
        elif choice == "4":
            save_corrections(CORRECTIONS_FILE, corrections)
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
