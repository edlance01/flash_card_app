from flask import Flask, render_template, request, redirect, url_for
import docx
import os
import tempfile

app = Flask(__name__)

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
            # Save the file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                file.save(tmp.name)
                temp_path = tmp.name
            # Process the saved file
            terms_and_definitions = extract_terms_and_definitions(temp_path)
            print(f"TERMS and DEFINITIONS")
            # Remove the temporary file
            os.remove(temp_path)
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


if __name__ == "__main__":

    #get_bullet_style("static/input_files/EssentialsOfAI_Module1_Vocab.docx")
    app.run(debug=True, port=5001)
