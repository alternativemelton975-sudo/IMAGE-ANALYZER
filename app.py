from flask import Flask, request, jsonify
from pathlib import Path
import json
from datetime import datetime

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
        return "❌ Image file not found."

    captions = {
        "simple": f"The image '{image_path.name}' was detected successfully.",
        "poetic": f"A visual masterpiece: {image_path.stem}, captured in {image_path.suffix[1:].upper()}.",
        "technical": f"File: {image_path.name} | Format: {image_path.suffix.upper()} | Path: {image_path.resolve()}",
        "playful": f"📸 Found a {image_path.suffix.upper()} treasure named '{image_path.stem}'!"
    }

    return captions.get(style, captions["simple"])


def get_image_details(path: str) -> dict:
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
        "created": datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
        "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    }


def batch_process_images(directory: str) -> list:
    dir_path = Path(directory)

    if not dir_path.exists() or not dir_path.is_dir():
        return []

    images = []

    for ext in SUPPORTED_FORMATS:
        images.extend(dir_path.glob(f"*{ext}"))
        images.extend(dir_path.glob(f"*{ext.upper()}"))

    return sorted(list(set(images)))


def generate_image_report(
    directory: str,
    output_file: str = "image_report.json"
) -> str:

    images = batch_process_images(directory)

    if not images:
        return f"❌ No images found in {directory}"

    report = {
        "directory": directory,
        "scan_date": datetime.now().isoformat(),
        "total_images": len(images),
        "images": [
            get_image_details(str(img))
            for img in images
        ]
    }

    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)

    return f"✅ Report generated: {output_file}"


@app.route("/")
def home():
    return jsonify({
        "application": "IMAGE-ANALYZER",
        "status": "running",
        "endpoints": {
            "GET /": "Application information",
            "GET /formats": "List supported formats",
            "POST /caption": "Generate image caption",
            "POST /details": "Get image details",
            "POST /report": "Generate directory report"
        }
    })


@app.route("/formats", methods=["GET"])
def formats():
    return jsonify({
        "supported_formats": SUPPORTED_FORMATS
    })


@app.route("/caption", methods=["POST"])
def caption():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON payload supplied"}), 400

    image_path = data.get("path")
    style = data.get("style", "simple")

    if not image_path:
        return jsonify({"error": "Path is required"}), 400

    return jsonify({
        "caption": image_to_caption(image_path, style)
    })


@app.route("/details", methods=["POST"])
def details():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON payload supplied"}), 400

    image_path = data.get("path")

    if not image_path:
        return jsonify({"error": "Path is required"}), 400

    return jsonify(get_image_details(image_path))


@app.route("/report", methods=["POST"])
def report():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON payload supplied"}), 400

    directory = data.get("directory", ".")

    result = generate_image_report(directory)

    return jsonify({
        "result": result
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
