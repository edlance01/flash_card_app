from flask import Flask, render_template, request, redirect, url_for
import os
import tempfile

app = Flask(__name__)
UPLOAD_FOLDER = "static/input_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_bullet_style(para):
    numPr = para._element.find(
            ".//w:numPr", namespaces=para._element.nsmap
        )

    return numPr


def extract_terms_and_definitions(doc_path):
    """
    Extracts terms and definitions from a plain text file.
    """
    with open(doc_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    terms_and_definitions = {}
    term = None
    definition = ""

    for line in lines:
        # Check for lines starting with a bullet point
        if line.startswith("•"):
            if term:  # Save the previous term and definition
                terms_and_definitions[term] = definition.strip()

            # Split the line into term and definition
            parts = line.split(":", 1)
            term = (
                parts[0].replace("•", "").strip()
            )  # Remove bullet point from the term

            # Ensure we extract the definition correctly
            definition = (
                parts[1].strip() if len(parts) > 1 else ""
            )  # Check for a definition after ':'
        elif term:  # Continue accumulating definition
            definition += " " + line.strip()

    if term:  # Add the last term and definition to the dictionary
        terms_and_definitions[term] = definition.strip()

    return terms_and_definitions


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main route for the flashcard program.
    """
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            print("\n***STARTING***")
            # Save the file directly to the mounted upload folder
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Process the saved file
            terms_and_definitions = extract_terms_and_definitions(file_path)
            print(f"TERMS and DEFINITIONS")

            # Optionally remove the file after processing if not needed
            # os.remove(file_path)

            return redirect(url_for("flashcards", terms=terms_and_definitions))
    return render_template("index.html")


@app.route("/flashcards")
def flashcards():
    """
    Route for displaying the flashcards.
    """
    terms_and_definitions = request.args.get("terms")
    if terms_and_definitions:
        terms_and_definitions = eval(terms_and_definitions)
        return render_template("flashcards.html", flashcards=terms_and_definitions)
    else:
        return redirect(url_for("index"))


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return f"File {file.filename} uploaded successfully", 200



