import os
import time
import shutil
import logging
import config
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from logger_setup import setup_logger

logger = setup_logger('logs/watcher.log', logging.DEBUG)

from transcriber import transcribe_file
from corrections import (
    load_corrections,
    apply_corrections,
    fuzzy_suggest_corrections,
    save_corrections
)

CORRECTION_FILE = config.CORRECTION_FILE
FUZZY_CORRECTION_FILE = "fuzzy_corrections.json"

from utils import extract_number, wait_for_files_to_finish, ensure_dir_exists

class FolderHandler(FileSystemEventHandler):
    def __init__(self, corrections, fuzzy_dict):
        self.corrections = corrections
        self.fuzzy_dict = fuzzy_dict

    def process_folder(self, folder_path):
        import manual_correct  # Imported here to avoid circular imports

        folder_name = os.path.basename(folder_path)
        print(f"\nNew folder detected: {folder_name}. Beginning transcription...\n")

        wait_for_files_to_finish(folder_path)

        wav_files = [f for f in os.listdir(folder_path) if f.upper().endswith(".WAV")]
        wav_files.sort(key=extract_number)

        transcriptions = {}
        for filename in wav_files:
            filepath = os.path.join(folder_path, filename)
            file_num = extract_number(filename)
            print(f"Transcribing {filename} as line {file_num:04d}...")
            text = transcribe_file(filepath)
            transcriptions[file_num] = text

        print("\nAll files transcribed. Applying dictionary corrections...\n")

        max_num = max(transcriptions.keys()) if transcriptions else 0
        corrected_lines = []

        for i in range(1, max_num + 1):
            raw_line = transcriptions.get(i, "")
            corrected_line = apply_corrections(raw_line, self.corrections)
            corrected_lines.append(f"{i:04d}\t{corrected_line}")

        ensure_dir_exists(config.PROCESSED_BASE)
        output_filename = f"{folder_name}.txt"
        output_path = os.path.join(config.PROCESSED_BASE, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(corrected_lines))

        print(f"\nAuto-corrected transcription saved to: {output_path}")

        save_corrections(CORRECTION_FILE, self.corrections)
        print("Corrections dictionary updated.")

        try:
            choice = input("\nDo you want to manually correct this transcript? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            choice = 'n'

        if choice == 'y':
            manual_correct.run_manual_review(output_path, self.corrections, self.fuzzy_dict)
            print("Manual correction complete.")
        else:
            print("Skipping manual correction.")

        archive_path = os.path.join(config.ARCHIVE_BASE, folder_name)
        shutil.move(folder_path, archive_path)
        print(f"Moved folder to archive: {archive_path}")

    def on_created(self, event):
        if event.is_directory:
            self.process_folder(event.src_path)

def start_watcher():
    corrections = load_corrections(CORRECTION_FILE)
    fuzzy_dict = load_corrections(FUZZY_CORRECTION_FILE)
    event_handler = FolderHandler(corrections, fuzzy_dict)
    observer = Observer()
    observer.schedule(event_handler, config.RAW_BASE, recursive=False)
    observer.start()
    print(f"Watching for new folders in: {config.RAW_BASE}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
