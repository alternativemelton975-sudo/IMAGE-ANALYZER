from flask import Flask, request, jsonify, send_file
from PIL import Image
from pathlib import Path
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audio"

Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(AUDIO_FOLDER).mkdir(exist_ok=True)

SUPPORTED_FORMATS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
    ".tiff"
}


def create_description(image_path):
    image = Image.open(image_path)

    width, height = image.size
    image_format = image.format

    return (
        f"This image is in {image_format} format. "
        f"It has a width of {width} pixels and a height of {height} pixels."
    )


@app.route("/")
def home():
    return """
    <h1>IMAGE TO AUDIO CONVERTER</h1>
    <p>Upload an image and receive an audio description.</p>

    <form action="/convert" method="post" enctype="multipart/form-data">
        <input type="file" name="image">
        <button type="submit">Convert</button>
    </form>
    """


@app.route("/convert", methods=["POST"])
def convert_image():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]

    if image_file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    extension = Path(image_file.filename).suffix.lower()

    if extension not in SUPPORTED_FORMATS:
        return jsonify({"error": "Unsupported image format"}), 400

    unique_id = str(uuid.uuid4())

    image_path = os.path.join(
        UPLOAD_FOLDER,
        f"{unique_id}{extension}"
    )

    image_file.save(image_path)

    description = create_description(image_path)

    audio_path = os.path.join(
        AUDIO_FOLDER,
        f"{unique_id}.mp3"
    )

    tts = gTTS(description)
    tts.save(audio_path)

    return send_file(
        audio_path,
        as_attachment=True,
        download_name="image_description.mp3"
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
