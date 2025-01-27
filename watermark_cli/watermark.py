import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple

def hex_to_rgba(hex_color: str) -> Tuple[int, int, int, int]:
    """Convert hex color in #RRGGBBAA or #RRGGBB format to RGBA tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 8:
        # RRGGBBAA format
        red = int(hex_color[0:2], 16)
        green = int(hex_color[2:4], 16)
        blue = int(hex_color[4:6], 16)
        alpha = int(hex_color[6:8], 16)
        return (red, green, blue, alpha)
    elif len(hex_color) == 6:
        # RRGGBB format (fully opaque)
        red = int(hex_color[0:2], 16)
        green = int(hex_color[2:4], 16)
        blue = int(hex_color[4:6], 16)
        return (red, green, blue, 255)
    else:
        raise ValueError("Invalid hex color format. Use #RRGGBBAA or #RRGGBB")

def add_watermark(
    image_path: str,
    text: str,
    size: int = 20,
    color: str = "#FFFFFF7F",  # 50% transparent white in RRGGBBAA format
    output_format: Optional[str] = None,
    output_folder: Optional[str] = None,
    postfix: str = "-wm"
) -> str:
    # Open image
    img = Image.open(image_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Create drawing context
    draw = ImageDraw.Draw(img)

    # Load font
    font = ImageFont.truetype("Arial", size)

    # Calculate text position (center)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2

    # Draw watermark
    rgba_color = hex_to_rgba(color)
    draw.text((x, y), text, font=font, fill=rgba_color)

    # Prepare output path
    input_path = Path(image_path)
    output_format = output_format or input_path.suffix[1:]
    output_name = f"{input_path.stem}{postfix}.{output_format}"

    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, output_name)
    else:
        output_path = os.path.join(input_path.parent, output_name)

    # Save image
    img.save(output_path, format=output_format.upper())
    return output_path
