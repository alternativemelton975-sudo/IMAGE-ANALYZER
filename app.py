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
   
