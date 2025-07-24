import time
import config
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from processor import process_folder

class FolderHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            print(f"New folder detected: {event.src_path}")
            process_folder(event.src_path, output_folder=config.PROCESSED_BASE)

def start_watcher(path_to_watch="."):
    observer = Observer()
    event_handler = FolderHandler()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()

    print(f"Watching folder: {path_to_watch}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping watcher.")
        observer.stop()
    observer.join()
