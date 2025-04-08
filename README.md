# Watermark CLI

A command-line tool to add text watermarks to images using ImageMagick.

## Installation

### Prerequisites
Make sure you have ImageMagick installed on your system. You can download it from [https://imagemagick.org/](https://imagemagick.org/).

### Install from local directory
```bash
pip install .
```

### Install directly from GitHub
```bash
pip install git+https://github.com/ShinChven/watermark.git
```

### Upgrade to the latest version
```bash
pip install --upgrade git+https://github.com/ShinChven/watermark.git
```

## Usage

```bash
watermark <image_path/folder_path> [OPTIONS]
```

### Options

- `--text TEXT`: Watermark text (required if not configured)
- `--size INTEGER`: Text size (default: 20)
- `--format TEXT`: Output image format
- `--folder PATH`: Output folder path (relative to input file's location or absolute path)
- `--postfix TEXT`: Output filename postfix (default: -wm)

### Examples

```bash
# Add watermark to single image
watermark image.jpg --text "Copyright 2023"

# Process all images in a directory
watermark ./images --text "Copyright" --size 30

# Specify output format and folder
watermark image.jpg --text "Copyright" --format png --folder ./output

# Save to a subfolder of the input file's location
watermark image.jpg --text "Copyright" --folder "watermarked"

# Save to an absolute path
watermark image.jpg --text "Copyright" --folder "/path/to/output"

# Save to a relative subfolder with format specified
watermark image.jpg --text "Copyright" --folder "output/jpg" --format jpg
```

## Configuration

Default options can be configured in `~/.config/watermark-cli/config.json`.
