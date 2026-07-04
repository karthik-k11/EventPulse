from flask import Flask, render_template, request
from monitor import start_monitoring, stop_monitoring, activity_log
import os

app = Flask(__name__)

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

    return render_template(
        "index.html",
        selected_folder=selected_folder,
        monitoring=monitoring,
        activity_log=activity_log
    )


if __name__ == "__main__":
    app.run(debug=True)