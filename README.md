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
- `--color TEXT`: Text color in #RRGGBBAA format (e.g., #FFFFFF7F for 50% transparent white)
- `--format TEXT`: Output image format
- `--folder PATH`: Output folder path (relative to input file's location or absolute path)
- `--postfix TEXT`: Output filename postfix (default: -wm)

### Examples

```bash
# Add watermark to single image with white text
watermark image.jpg --text "Copyright 2023" --color "#FFFFFFFF"

# Add watermark with 50% transparent red text
watermark image.jpg --text "Copyright" --color "#FF00007F"

# Add watermark with 30% transparent black text
watermark image.jpg --text "Copyright" --color "#000000B3"

# Process all images in a directory
watermark ./images --text "Copyright" --size 30 --color "#80FF0000"

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
