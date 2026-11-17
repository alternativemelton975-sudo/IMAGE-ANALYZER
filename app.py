from pathlib import Path
from PIL import Image
from gtts import gTTS


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


def image_to_audio(image_path):
    image_path = Path(image_path)

    if not image_path.exists():
        print("Image not found.")
        return

    if image_path.suffix.lower() not in SUPPORTED_FORMATS:
        print("Unsupported image format.")
        return

    description = describe_image(image_path)

    print("\nDescription:")
    print(description)

    output_file = f"{image_path.stem}.mp3"

    tts = gTTS(text=description, lang="en")
    tts.save(output_file)

    print(f"\nAudio saved as: {output_file}")


if __name__ == "__main__":

    print("=== IMAGE TO AUDIO CONVERTER ===\n")

    image_path = input(
        "Enter image path: "
    ).strip()

    image_to_audio(image_path)
