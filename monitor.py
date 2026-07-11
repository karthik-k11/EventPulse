from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from datetime import datetime
from rules import apply_rule
from db import save_event

observer = None

activity_log = []


def add_event(event_name, file_name, action):
    activity_log.insert(0, {
        "time": datetime.now().strftime("%H:%M:%S"),
        "event": event_name,
        "file": file_name,
        "action": action
    })
    save_event(
        datetime.now().strftime("%H:%M:%S"),
        event_name,
        file_name,
        action
    )

    if len(activity_log) > 20:
        activity_log.pop()


class EventHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:

            file_name = Path(event.src_path).name

            print(f"[CREATED] {event.src_path}")

            action = apply_rule(event.src_path)

            add_event("Created", file_name, action)

    def on_deleted(self, event):
        if not event.is_directory:
            file_name = Path(event.src_path).name
            print(f"[DELETED] {event.src_path}")
            add_event("Deleted", file_name, "No Action")

    def on_modified(self, event):
        if not event.is_directory:
            file_name = Path(event.src_path).name
            print(f"[MODIFIED] {event.src_path}")
            add_event("Modified", file_name, "No Action")

    def on_moved(self, event):
        if not event.is_directory:

            old_name = Path(event.src_path).name
            new_name = Path(event.dest_path).name

            print(f"[RENAMED] {event.src_path} -> {event.dest_path}")

            action = apply_rule(event.dest_path)

            add_event(
                "Renamed",
                f"{old_name} → {new_name}",
                action
            )


def start_monitoring(folder_path):
    global observer

    if observer is not None:
        return

    event_handler = EventHandler()

    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()

    print(f"\nMonitoring started: {folder_path}")


def stop_monitoring():
    global observer

    if observer is not None:
        observer.stop()
        observer.join()
        observer = None

        print("\nMonitoring stopped.")