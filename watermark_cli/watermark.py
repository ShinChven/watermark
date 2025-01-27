import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple

def add_watermark(
    image_path: str,
    text: str,
    size: int = 20,
    format: Optional[str] = None,
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
    font_path = "Arial"
    try:
        font = ImageFont.truetype(font_path, size)
        print(f"Using font path: {font.path}")
    except IOError:
        font = ImageFont.load_default()
        print(f"Using default font: {font.getname()}")

    # Calculate text position (center)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2

    # Draw watermark
    draw.text((x, y), text, font=font)

    # Prepare output path
    input_path = Path(image_path)
    output_format = format or input_path.suffix[1:]
    output_name = f"{input_path.stem}{postfix}.{output_format}"

    if output_folder:
        output_dir = input_path.parent / Path(output_folder)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_name
    else:
        output_path = input_path.parent / output_name

    # Save image
    img.save(str(output_path), format=output_format.upper())
    return str(output_path)
