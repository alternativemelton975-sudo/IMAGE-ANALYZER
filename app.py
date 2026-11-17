from flask import Flask, request, send_file
from pathlib import Path
from PIL import Image
from gtts import gTTS
import uuid
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audio"

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

if not os.path.exists(AUDIO_FOLDER):
    os.mkdir(AUDIO_FOLDER)

SUPPORTED_FORMATS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
    ".tiff"
}


def describe_image(image_path):
    image = Image.open(image_path)

    width, height = image.size
    image_format = image.format

    return (
        f"This image is a {image_format} image. "
        f"It is {width} pixels wide and "
        f"{height} pixels tall."
    )


@app.route("/")
def home():
    return "Image To Audio Converter is running."


@app.route("/convert", methods=["POST"])
def convert():

    if "image" not in request.files:
        return "No image uploaded", 400

    image_file = request.files["image"]

    if image_file.filename == "":
        return "No file selected", 400

    extension = Path(image_file.filename).suffix.lower()

    if extension not in SUPPORTED_FORMATS:
        return "Unsupported image format", 400

    unique_id = str(uuid.uuid4())

    image_path = os.path.join(
        UPLOAD_FOLDER,
        f"{unique_id}{extension}"
    )

    image_file.save(image_path)

    description = describe_image(image_path)

    audio_path = os.path.join(
        AUDIO_FOLDER,
        f"{unique_id}.mp3"
    )

    tts = gTTS(text=description, lang="en")
    tts.save(audio_path)

    return send_file(
        audio_path,
        as_attachment=True,
        download_name="image_description.mp3"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
