# Watermark CLI

A command-line tool to add text watermarks to images.

## Installation

```bash
pip install .
```

## Usage

```bash
watermark <image_path/folder_path> [OPTIONS]
```

### Options

- `--text TEXT`: Watermark text (required if not configured)
- `--size INTEGER`: Text size (default: 20)
- `--color TEXT`: Text color in ARGB hex format (default: #80FFFFFF)
- `--output TEXT`: Output image format
- `--folder PATH`: Output folder path
- `--postfix TEXT`: Output filename postfix (default: -wm)

### Examples

```bash
# Add watermark to single image
watermark image.jpg --text "Copyright 2023"

# Process all images in a directory
watermark ./images --text "Copyright" --size 30 --color "#80FF0000"

# Specify output format and folder
watermark image.jpg --text "Copyright" --output png --folder ./output
```

## Configuration

Default options can be configured in `~/.config/watermark-cli/config.json`.
