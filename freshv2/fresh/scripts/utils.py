import os
import time

def extract_number(filename):
    base = os.path.splitext(filename)[0]
    return int(base[-4:]) if base[-4:].isdigit() else 0

def wait_for_files_to_finish(folder_path, wait_time=3):
    prev_files = set()
    while True:
        current_files = set(os.listdir(folder_path))
        if current_files == prev_files and current_files:
            break
        prev_files = current_files
        time.sleep(wait_time)

def ensure_dir_exists(path):
    os.makedirs(path, exist_ok=True)
