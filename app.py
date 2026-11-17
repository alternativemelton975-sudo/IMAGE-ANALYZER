from flask import Flask, jsonify, request
from pathlib import Path
from datetime import datetime
import json

app = Flask(__name__)

SUPPORTED_FORMATS = [
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
    '.bmp',
    '.webp',
    '.svg',
    '.tiff'
]


def image_to_caption(path: str, style: str = "simple") -> str:
    image_path = Path(path)

    if not image_path.exists():
        return "Image file not found."

    captions = {
        "simple": f"The image '{image_path.name}' was detected successfully.",
        "poetic": f"A visual masterpiece: {image_path.stem}, captured in {image_path.suffix[1:].upper()}.",
        "technical": f"File: {image_path.name} | Format: {image_path.suffix.upper()}",
        "playful": f"Found a {image_path.suffix.upper()} treasure named '{image_path.stem}'!"
    }

    return captions.get(style, captions["simple"])


def get_image_details(path: str):
    image_path = Path(path)

    if not image_path.exists():
        return {"error": "File not found"}

    if image_path.suffix.lower() not in SUPPORTED_FORMATS:
        return {"error": f"Unsupported format: {image_path.suffix}"}

    stats = image_path.stat()

    return {
        "filename": image_path.name,
        "format": image_path.suffix[1:].upper(),
        "size_bytes": stats.st_size,
        "size_mb": round(stats.st_size / (1024 * 1024), 2),
        "created": datetime.fromtimestamp(
            stats.st_ctime
        ).strftime("%Y-%m-%d %H:%M:%S"),
        "modified": datetime.fromtimestamp(
            stats.st_mtime
        ).strftime("%Y-%m-%d %H:%M:%S")
    }


@app.route("/")
def home():
    return jsonify({
        "application": "IMAGE-ANALYZER",
        "status": "running"
    })


@app.route("/formats")
def formats():
    return jsonify({
        "supported_formats": SUPPORTED_FORMATS
    })


@app.route("/caption", methods=["POST"])
def caption():

    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    image_path = data.get("path")
    style = data.get("style", "simple")

    return jsonify({
        "caption": image_to_caption(image_path, style)
    })


@app.route("/details", methods=["POST"])
def details():

    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    image_path = data.get("path")

    return jsonify(get_image_details(image_path))


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
