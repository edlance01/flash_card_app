from flask import Flask, render_template, request, redirect, url_for
import os
import time

app = Flask(__name__)
print("starting...", flush=True)
UPLOAD_FOLDER = os.path.join(app.static_folder, "input_files")
print(f"UPLOAD folder is:{UPLOAD_FOLDER}", flush=True)
# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def extract_terms_and_definitions(doc_path):
    print(f"Entering extract_terms_and_definitions for: {doc_path}", flush=True)
    try:
        start_time = time.time()

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

        print(f"Processing took {time.time() - start_time:.2f} seconds.", flush=True)
        return terms_and_definitions
    except FileNotFoundError:
        print(f"File not found: {doc_path}", flush=True)
        return {}
    except Exception as e:
        print(f"Error parsing file: {doc_path}, {e}", flush=True)
        return {}


@app.route("/", methods=["GET"])
def index():
    """Main route for displaying the list of files."""
    files = os.listdir(UPLOAD_FOLDER)
    files.sort()  # Sort the files alphabetically
    return render_template("index.html", files=files)


# @app.route("/flashcards/<filename>")
# def flashcards(filename):
#     """Route for displaying the flashcards."""
#     file_path = os.path.join(UPLOAD_FOLDER, filename)
#     if os.path.exists(file_path):
#         terms_and_definitions = extract_terms_and_definitions(file_path)
#         return render_template("flashcards.html", flashcards=terms_and_definitions)
#     else:
#         return redirect(url_for("index"))


@app.route("/flashcards/<filename>")
def flashcards(filename):
    print(f"Accessing flashcards for: {filename}", flush=True)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    print(f"File path: {file_path}", flush=True)
    if os.path.exists(file_path):
        print("File exists, processing...", flush=True)
        terms_and_definitions = extract_terms_and_definitions(file_path)
        print("Terms and definitions extracted.", flush=True)
        return render_template("flashcards.html", flashcards=terms_and_definitions)
    else:
        print("File not found.", flush=True)
        return redirect(url_for("index"))
