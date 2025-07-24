import json
import os

CORRECTIONS_FILE = "corrections.json"

def load_corrections(path=CORRECTIONS_FILE):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Invalid JSON in corrections file. Starting fresh.")
    return {}

def save_corrections(corrections, path=CORRECTIONS_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(corrections, f, indent=2, ensure_ascii=False)
