from flask import Flask, render_template, request
from monitor import start_monitoring, stop_monitoring, activity_log
import os
from config import create_destination_folders
from db import initialize_database
from collections import Counter
from pathlib import Path

app = Flask(__name__)

create_destination_folders()
initialize_database()

selected_folder = ""
monitoring = False


@app.route("/", methods=["GET", "POST"])
def home():
    global selected_folder
    global monitoring

    if request.method == "POST":

        action = request.form.get("action")

        if action == "save":
            selected_folder = request.form.get("folder_path", "").strip()

            selected_folder = selected_folder.strip('"')

        elif action == "start":

            if (
                selected_folder
                and os.path.isdir(selected_folder)
                and not monitoring
            ):
                start_monitoring(selected_folder)
                monitoring = True

        elif action == "stop":

            if monitoring:
                stop_monitoring()
                monitoring = False

    files_processed = len(activity_log)

    events_detected = len(activity_log)

    total_actions = sum(
        1 for item in activity_log
        if item["action"] != "No Action"
    )

    extensions = []

    for item in activity_log:

       file_name = item["file"]

       if "→" in file_name:
            file_name = file_name.split("→")[-1].strip()

       extension = Path(file_name).suffix.lower()

       if extension:
            extensions.append(extension)

    if extensions:
        most_common_file_type = Counter(extensions).most_common(1)[0][0]
    else:
        most_common_file_type = "-"

    return render_template(
        "index.html",
        selected_folder=selected_folder,
        monitoring=monitoring,
        activity_log=activity_log,
        files_processed=files_processed,
        events_detected=events_detected,
        most_common_file_type=most_common_file_type,
        total_actions=total_actions
    )


if __name__ == "__main__":
    app.run(debug=True)