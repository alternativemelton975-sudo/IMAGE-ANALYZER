# Image Analyzer

A Python utility for analyzing image metadata, generating detailed reports, and batch processing image directories.

## Features

- **Single Image Analysis** - Get detailed metadata about an image
- **Image Captions** - Generate captions in different styles (simple, poetic, technical, playful)
- **Batch Processing** - Process all images in a directory
- **JSON Reports** - Generate comprehensive image reports
- **Format Support** - JPG, PNG, GIF, BMP, WebP, SVG, TIFF

## Requirements

- Python 3.11+
- No external dependencies (uses only standard library)

## Installation

```bash
git clone https://github.com/yourusername/image-analyzer.git
cd image-analyzer
python Image2Audio.py
```

## Usage

```bash
python Image2Audio.py
```

### Menu Options

1. **Analyze Single Image** - Generate caption for an image
2. **Get Detailed Info** - Show full metadata
3. **Batch Process Directory** - Process all images and create report
4. **Supported Formats** - List all supported image formats

## Example

```bash
$ python Image2Audio.py
=== IMAGE ANALYZER ===

1. Analyze single image
2. Get detailed info
3. Batch process directory
4. Supported formats

Choose option (1-4): 2
Enter image path: photo.jpg

========================================
Filename: photo.jpg
Format: JPG
Size Bytes: 245382
Size Mb: 0.23
Created: 2025-01-15 10:30
Modified: 2025-01-15 10:30
========================================
```

## Docker

```bash
docker build -t image-analyzer .
docker run -it image-analyzer:latest
```

## License

MIT
