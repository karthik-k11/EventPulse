from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from pathlib import Path
from datetime import datetime

from rules import apply_rule
from db import save_event

observer = None

activity_log = []


def add_activity(file_name, action):

    activity_log.insert(
        0,
        {
            "time": datetime.now().strftime("%I:%M %p"),
            "file": file_name,
            "action": action
        }
    )

    if len(activity_log) > 20:
        activity_log.pop()

    save_event(
        datetime.now().strftime("%I:%M %p"),
        file_name,
        action
    )


class EventHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        if Path(event.src_path).suffix.lower() == ".txt":
            return

        action = apply_rule(event.src_path)

        file_name = Path(event.src_path).name

        add_activity(
            file_name,
            action
        )

        print(f"[AUTOMATION] {file_name} -> {action}")

    def on_moved(self, event):

        if event.is_directory:
            return

        new_file = Path(event.dest_path)

        action = apply_rule(event.dest_path)

        add_activity(
            new_file.name,
            action
        )

        print(f"[AUTOMATION] {new_file.name} -> {action}")

    ##To ignore modified
    def on_modified(self, event):
        pass
    ##To ignore deleted
    def on_deleted(self, event):
        pass


def start_monitoring(folder_path):

    global observer

    if observer is not None:
        return

    event_handler = EventHandler()

    observer = Observer()

    observer.schedule(
        event_handler,
        folder_path,
        recursive=False
    )

    observer.start()

    print(f"\nMonitoring Started : {folder_path}")


def stop_monitoring():

    global observer

    if observer is not None:

        observer.stop()

        observer.join()

        observer = None

        print("\nMonitoring Stopped")