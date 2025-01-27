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
@click.option('--color', help='Text color in ARGB hex format (e.g., #80FFFFFF)')
@click.option('--output', help='Output image format')
@click.option('--folder', type=click.Path(), help='Output folder path')
@click.option('--postfix', help='Output filename postfix')
def main(
    path: str,
    text: Optional[str],
    size: Optional[int],
    color: Optional[str],
    output: Optional[str],
    folder: Optional[str],
    postfix: Optional[str]
):
    """Add text watermark to images."""
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
        'output_format': output or config['output'],
        'output_folder': folder or config['folder'],
        'postfix': postfix or config['postfix']
    }

    if os.path.isfile(path):
        output_path = add_watermark(path, **options)
        click.echo(f"Watermark added: {output_path}")
    else:
        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    file_path = os.path.join(root, file)
                    output_path = add_watermark(file_path, **options)
                    click.echo(f"Watermark added: {output_path}")

if __name__ == '__main__':
    main()
