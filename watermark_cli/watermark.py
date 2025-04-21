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

    # Determine gravity and offset based on position and padding
    gravity_map = {
        "center": "Center",
        "top-left": "NorthWest",
        "top-right": "NorthEast",
        "bottom-left": "SouthWest",
        "bottom-right": "SouthEast",
        "top-center": "North",      # Added
        "bottom-center": "South",   # Added
        "left-center": "West",      # Added
        "right-center": "East",     # Added
    }
    gravity = gravity_map.get(position, "SouthEast")  # Default if invalid

    offset_x = 0
    offset_y = 0
    if position == "center":
        annotate_offset = "+0+0"
    elif "left" in position:
        offset_x = padding
    elif "right" in position:
        offset_x = padding
    # No horizontal offset adjustment needed for top-center or bottom-center

    if "top" in position:
        offset_y = padding
    elif "bottom" in position:
        offset_y = padding
    # No vertical offset adjustment needed for left-center or right-center

    # Adjust sign based on gravity for annotate offset
    if gravity in ["NorthEast", "SouthEast", "East"]:
        offset_x = f"+{offset_x}"
    elif gravity in ["NorthWest", "SouthWest", "West"]:
        offset_x = f"+{offset_x}" # ImageMagick needs + for left/west offset too
    elif gravity in ["North", "South", "Center"]:
         offset_x = f"+{offset_x}" # Center needs explicit sign if non-zero (though it's 0 here)


    if gravity in ["SouthWest", "SouthEast", "South"]:
        offset_y = f"+{offset_y}"
    elif gravity in ["NorthWest", "NorthEast", "North"]:
        offset_y = f"+{offset_y}" # ImageMagick needs + for top/north offset too
    elif gravity in ["West", "East", "Center"]:
         offset_y = f"+{offset_y}" # Center needs explicit sign if non-zero (though it's 0 here)


    # Handle specific center cases for annotate offset string
    if position == "center":
        annotate_offset = "+0+0"
    elif position == "top-center":
        annotate_offset = f"+0{offset_y}"
    elif position == "bottom-center":
        annotate_offset = f"+0{offset_y}"
    elif position == "left-center":
        annotate_offset = f"{offset_x}+0"
    elif position == "right-center":
        annotate_offset = f"{offset_x}+0"
    elif position in ["top-left", "top-right", "bottom-left", "bottom-right"]:
         # Use calculated offsets for corners
         annotate_offset = f"{offset_x}{offset_y}"
    else: # Default fallback (shouldn't happen with click.Choice)
        annotate_offset = f"+{padding}+{padding}"


    # Construct the ImageMagick command
    command = [
        "magick",
        image_path,
        "-gravity",
        gravity,
        "-pointsize",
        str(size),
        "-fill",
        color,
        "-annotate",
        annotate_offset,
        text,
        str(output_path),
    ]

    # Execute the command
    try:
        subprocess.run(command, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing ImageMagick: {e.stderr.decode()}")
        raise

    return str(output_path)
