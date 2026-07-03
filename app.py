from flask import Flask, render_template, request

app = Flask(__name__)

selected_folder = ""


@app.route("/", methods=["GET", "POST"])
def home():
    global selected_folder

    if request.method == "POST":
        selected_folder = request.form.get("folder_path", "").strip()

    return render_template(
        "index.html",
        selected_folder=selected_folder
    )


if __name__ == "__main__":
    app.run(debug=True)