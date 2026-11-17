from flask import Flask, request, send_file

from pathlib import Path
from PIL import Image
from gtts import gTTS

import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

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
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image To Audio Converter</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                text-align: center;
            }

            h1 {
                color: #333;
            }

            form {
                margin-top: 20px;
            }

            button {
                padding: 10px 20px;
                margin-top: 10px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>

        <h1>Image To Audio Converter</h1>

        <p>Upload an image and receive an MP3 description.</p>

        <form action="/convert" method="post" enctype="multipart/form-data">

            <input
                type="file"
                name="image"
                accept=".jpg,.jpeg,.png,.gif,.bmp,.webp,.tiff"
                required
            >

            <br><br>

            <button type="submit">
                Convert To Audio
            </button>

        </form>

    </body>
    </html>
    """


@app.route("/convert", methods=["POST"])
def convert():

    if "image" not in request.files:
        return "No image uploaded.", 400

    image_file = request.files["image"]

    if image_file.filename == "":
        return "No file selected.", 400

    extension = Path(image_file.filename).suffix.lower()

    if extension not in SUPPORTED_FORMATS:
        return "Unsupported image format.", 400

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

    tts = gTTS(
        text=description,
        lang="en"
    )

    tts.save(audio_path)

    return send_file(
        audio_path,
        as_attachment=True,
        download_name="image_description.mp3"
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
