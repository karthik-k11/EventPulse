from pathlib import Path
import shutil

from config import DESTINATION_FOLDERS


def apply_rule(file_path):
    source = Path(file_path)

    if not source.exists():
        return "No Action"

    extension = source.suffix.lower()

    if extension == ".pdf":
        destination_folder = DESTINATION_FOLDERS["documents"]
        action = "Moved to Documents"

    elif extension == ".csv":
        destination_folder = DESTINATION_FOLDERS["data"]
        action = "Moved to Data"

    elif extension in [".jpg", ".jpeg", ".png", ".gif"]:
        destination_folder = DESTINATION_FOLDERS["images"]
        action = "Moved to Images"

    else:
        return "No Rule Matched"

    destination = destination_folder / source.name

    shutil.move(str(source), str(destination))

    return action