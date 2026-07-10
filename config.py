from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

WATCH_FOLDER = ""

DESTINATION_FOLDERS = {
    "documents": BASE_DIR / "Documents",
    "data": BASE_DIR / "Data",
    "images": BASE_DIR / "Images"
}


def create_destination_folders():
    for folder in DESTINATION_FOLDERS.values():
        folder.mkdir(exist_ok=True)