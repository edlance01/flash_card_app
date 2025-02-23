from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.static_folder, "input_files")

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def extract_terms_and_definitions(doc_path):
    """Extracts terms and definitions from a plain text file."""
    with open(doc_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    terms_and_definitions = {}
    term = None
    definition = ""

    for line in lines:
        if line.startswith("•"):
            if term:
                terms_and_definitions[term] = definition.strip()

            parts = line.split(":", 1)
            term = parts[0].replace("•", "").strip()  # Fix: Extract the first element
            definition = parts[1].strip() if len(parts) > 1 else ""  # Extract definition safely
        elif term:
            definition += " " + line.strip()

    if term:
        terms_and_definitions[term] = definition.strip()


    return terms_and_definitions


@app.route("/", methods=["GET"])
def index():
    """Main route for displaying the list of files."""
    files = os.listdir(UPLOAD_FOLDER)
    files.sort()  # Sort the files alphabetically
    return render_template("index.html", files=files)


@app.route("/flashcards/<filename>")
def flashcards(filename):
    """Route for displaying the flashcards."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        terms_and_definitions = extract_terms_and_definitions(file_path)
        return render_template("flashcards.html", flashcards=terms_and_definitions)
    else:
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
