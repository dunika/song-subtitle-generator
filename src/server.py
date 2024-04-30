import os

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

import captions

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def upload_form():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files["file"]

    safe_filename = secure_filename(file.filename)

    temp = os.path.join(app.config["UPLOAD_FOLDER"], safe_filename)
    file.save(temp)

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    captions_config = captions.get(temp)

    return jsonify(captions_config), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
