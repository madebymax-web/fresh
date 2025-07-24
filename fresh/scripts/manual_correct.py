import json
import os

CORRECTIONS_FILE = "corrections.json"
FUZZY_FILE = "fuzzy_corrections.json"

def load_corrections(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Invalid JSON file at {path}. Starting with empty dictionary.")
    return {}

def save_corrections(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved corrections to {path}")

def manual_edit_transcription(lines, correction_dict, batch_size=10):
    total_lines = len(lines)
    i = 0

    while i < total_lines:
        batch_end = min(i + batch_size, total_lines)
        print(f"\nShowing lines {i+1} to {batch_end}:")

        # Display batch lines with their line numbers and content
        for idx in range(i, batch_end):
            line_stripped = lines[idx].strip()
            if not line_stripped or "\t" not in line_stripped:
                print(f"{idx+1}: [skipped - malformed or empty]")
            else:
                line_num, content = line_stripped.split("\t", 1)
                print(f"{idx+1}: Line {line_num} - {content}")

        user_input = input("\nEnter line number to edit, Enter to skip, or 'q' to quit: ").strip()
        if user_input.lower() == 'q':
            print("Exiting manual edit early.")
            break
        if not user_input:
            i += batch_size
            continue

        try:
            chosen_index = int(user_input) - 1
            if chosen_index < i or chosen_index >= batch_end:
                print("Line number not in current batch. Try again.")
                continue
        except ValueError:
            print("Invalid input. Enter a valid line number, Enter, or 'q'.")
            continue

        line_stripped = lines[chosen_index].strip()
        line_num, content = line_stripped.split("\t", 1)
        print(f"\nEditing Line {line_num}: {content}")
        new_content = input("Enter corrected line content: ").strip()
        if new_content and new_content != content:
            lines[chosen_index] = f"{line_num}\t{new_content}\n"
            add_to_dict = input("Add this correction to dictionary? (y/n): ").strip().lower()
            if add_to_dict == "y":
                correction_dict[content] = new_content
                print(f"Added to dictionary: '{content}' -> '{new_content}'")
        else:
            print("No changes made to this line.")

    return lines

def run_manual_review(filepath, correction_dict, fuzzy_dict):
    print("\nStarting manual review...")

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = manual_edit_transcription(lines, correction_dict)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    save_corrections(CORRECTIONS_FILE, correction_dict)
    save_corrections(FUZZY_FILE, fuzzy_dict)

    print("\nManual review finished and saved.")

if __name__ == "__main__":
    # Example usage - update these as needed
    transcription_path = input("Enter path to transcription file: ").strip()
    corrections = load_corrections(CORRECTIONS_FILE)
    fuzzy = load_corrections(FUZZY_FILE)

    run_manual_review(transcription_path, corrections, fuzzy)
