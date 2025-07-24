from dictionary import load_corrections, save_corrections

def manual_review(transcript_path):
    corrections = load_corrections()
    with open(transcript_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    batch_size = 10
    idx = 0
    total = len(lines)

    while idx < total:
        batch = lines[idx:idx+batch_size]

        print("\n--- Transcript Lines ---")
        for i, line in enumerate(batch, start=idx+1):
            print(f"{i}: {line.strip()}")

        user_input = input("\nEnter line number(s) to correct (comma separated), or press Enter to skip batch: ").strip()
        if not user_input:
            idx += batch_size
            continue

        to_fix = [int(x.strip()) for x in user_input.split(",") if x.strip().isdigit()]

        for line_num in to_fix:
            if line_num < 1 or line_num > total:
                print(f"Line {line_num} is out of range.")
                continue
            original_line = lines[line_num-1].strip()
            print(f"\nOriginal: {original_line}")

            # Extract words from the line to show
            parts = original_line.split("\t")
            if len(parts) < 2:
                print("Malformed line, skipping.")
                continue
            key, text = parts[0], parts[1]

            print(f"Transcript Text: {text}")

            while True:
                wrong_word = input("Enter the incorrect word or phrase (or 'done' to finish this line): ").strip()
                if wrong_word.lower() == "done":
                    break
                if wrong_word not in text:
                    print(f"'{wrong_word}' not found in line text. Try again.")
                    continue
                corrected_word = input(f"Enter the correction for '{wrong_word}': ").strip()
                text = text.replace(wrong_word, corrected_word)
                corrections[wrong_word] = corrected_word
                print(f"Updated line: {text}")

            lines[line_num-1] = f"{key}\t{text}\n"

        idx += batch_size

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    save_corrections(corrections)
    print("Manual review complete and corrections saved.")
