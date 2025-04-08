import os
import subprocess
from pathlib import Path
from typing import Optional

def add_watermark(
    image_path: str,
    text: str,
    size: int,
    color: str,
    position: str,
    postfix: str,
    padding: int,
    format: Optional[str] = None,
    output_folder: Optional[str] = None
) -> str:
    """Adds a text watermark to an image using ImageMagick."""

    input_path = Path(image_path)
    output_format = format or input_path.suffix[1:]
    output_name = f"{input_path.stem}{postfix}.{output_format}"

    if output_folder:
        output_dir = input_path.parent / Path(output_folder)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_name
    else:
        output_path = input_path.parent / output_name

    # Determine gravity based on position
    if position == "center":
        gravity = "center"
        offset = "+0+0"
    elif position == "top-left":
        gravity = "northwest"
        offset = f"+{padding}+{padding}"
    elif position == "top-right":
        gravity = "northeast"
        offset = f"+{padding}+{padding}"
    elif position == "bottom-left":
        gravity = "southwest"
        offset = f"+{padding}+{padding}"
    elif position == "bottom-right":
        gravity = "southeast"
        offset = f"+{padding}+{padding}"
    else:
        gravity = "center"
        offset = "+0+0"

    # Construct the ImageMagick command
    command = [
        "magick",
        image_path,
        "-gravity", gravity,
        "-pointsize", str(size),
        "-fill", color,
        "-annotate", offset, text,
        str(output_path)
    ]

    # Execute the command
    try:
        subprocess.run(command, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing ImageMagick: {e.stderr.decode()}")
        raise

    return str(output_path)
