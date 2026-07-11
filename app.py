from flask import Flask, render_template, request
from collections import Counter
from pathlib import Path
import os

from monitor import (
    start_monitoring,
    stop_monitoring,
    activity_log
)

from config import create_destination_folders
from db import (
    initialize_database,
    get_history
)

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

            selected_folder = request.form.get(
                "folder_path",
                ""
            ).strip().strip('"')

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

    automations_completed = sum(
        1
        for item in activity_log
        if item["action"] != "No Rule Matched"
    )

    files_skipped = sum(
        1
        for item in activity_log
        if item["action"] == "No Rule Matched"
    )

    processed_extensions = []

    for item in activity_log:

        if item["action"] == "No Rule Matched":
            continue

        extension = Path(item["file"]).suffix.lower()

        if extension:
            processed_extensions.append(extension)

    if processed_extensions:

        most_processed_type = Counter(
            processed_extensions
        ).most_common(1)[0][0].replace(".", "").upper()

    else:

        most_processed_type = "-"

    return render_template(

        "index.html",

        selected_folder=selected_folder,

        monitoring=monitoring,

        activity_log=activity_log,

        files_processed=files_processed,

        automations_completed=automations_completed,

        files_skipped=files_skipped,

        most_processed_type=most_processed_type

    )


@app.route("/history")
def history():

    history_data = get_history()

    return render_template(

        "history.html",

        history_data=history_data

    )


if __name__ == "__main__":

    app.run(debug=True)