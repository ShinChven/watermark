import click
import os
from pathlib import Path
from typing import Optional
from .config import load_config
from .watermark import add_watermark

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--text', help='Watermark text')
@click.option('--size', type=int, help='Text size')
@click.option('--color', type=str, help='Text color (e.g., rgba(255,255,255,0.3))')
@click.option('--position', type=click.Choice(['center', 'top-left', 'top-right', 'bottom-left', 'bottom-right']), help='Watermark position')
@click.option('--folder', type=click.Path(), help='Output folder path')
@click.option('--postfix', help='Output filename postfix')
@click.option('--padding', type=int, help='Padding for corner positions')
@click.option('--format', 'format', help='Output image format')
def main(
    path: str,
    text: Optional[str],
    size: Optional[int],
    color: Optional[str],
    position: Optional[str],
    folder: Optional[str],
    postfix: Optional[str],
    padding: Optional[int],
    format: Optional[str]
):
    """Add text watermark to images using ImageMagick."""

    # Load config outside the loop
    config = load_config()

    # Merge CLI options with config
    text = text or config['text']
    if not text:
        click.echo("Error: Watermark text not provided and not found in config", err=True)
        return 1

    options = {
        'text': text,
        'size': size or config['size'],
        'color': color or config['color'],
        'position': position or config['position'],
        'postfix': postfix or config['postfix'],
        'padding': padding or config['padding'],
        'format': format or config['format'],
        'output_folder': folder or config['folder'],
    }

    # Process files
    if os.path.isfile(path):
        output_path = add_watermark(path, **options)
        click.echo(f"Watermark added: {output_path}")
    else:
        # Process files in the top-level directory only
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path) and file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                # Check if the file is already watermarked
                if options['postfix'] not in file:
                    output_path = add_watermark(file_path, **options)
                    click.echo(f"Watermark added: {output_path}")
                else:
                    click.echo(f"Skipping already watermarked file: {file_path}")

if __name__ == '__main__':
    main()
