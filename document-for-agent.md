# Project Analysis: watermark-cli

## Overview

This project, `watermark-cli`, is a command-line interface (CLI) tool developed in Python. Its primary function is to add text watermarks to image files. It leverages the external ImageMagick library (specifically the `magick` command) to perform the image manipulation. The tool uses the Click library for creating the CLI and Poetry for dependency management and packaging.

## Core Features

1.  **Text Watermarking:** Adds user-defined text onto images.
2.  **Customization:** Allows configuration of watermark text, size, color (including transparency via RGBA or hex with alpha), position (center, corners: `top-left`, `top-right`, `bottom-left`, `bottom-right`, and edges: `top-center`, `bottom-center`, `left-center`, `right-center`), padding from corners/edges, output filename postfix, and output image format.
3.  **Configuration File:** Persists user preferences (like default text, color, size, etc.) in a JSON file (`~/.config/watermark-cli/config.json`). Creates this file with defaults if it does not exist.
4.  **CLI Overrides:** Command-line arguments take precedence over settings in the configuration file.
5.  **Input Handling:** Accepts either a single image file path or a directory path as input.
6.  **Directory Processing:** When given a directory, it processes image files (`.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp`) found directly within that directory (non-recursive).
7.  **Idempotency Check:** Avoids re-watermarking files by checking if the output filename postfix already exists in the filename.
8.  **Output Location:** Saves watermarked images in the same directory as the original by default, or in a specified output sub-directory.

## File Breakdown

1.  **`pyproject.toml`**:
    -   Defines project metadata (name, version, description, author).
    -   Specifies Python version and dependencies (`click`).
    *   Declares the script entry point: the `watermark` command executes `watermark_cli.cli:main`.
    -   Configures the build system (Poetry).

2.  **`watermark_cli/config.py`**:
    -   Manages the loading and saving of user configuration from/to `~/.config/watermark-cli/config.json`.
    -   Defines `DEFAULT_CONFIG` containing default values for all settings.
    -   `load_config()`: Reads the JSON config, merges it with defaults (user config overrides defaults), and returns the resulting dictionary. Creates the config file/directory if they don't exist.
    -   `save_config()`: Writes a given configuration dictionary to the JSON file.

3.  **`watermark_cli/watermark.py`**:
    -   Contains the core watermarking logic in the `add_watermark` function.
    -   Takes image path and all watermark parameters as arguments.
    -   Constructs the output file path based on input path, postfix, format, and optional output folder. Creates the output folder if necessary.
    -   Translates the abstract position name (e.g., "bottom-right") into ImageMagick's `gravity` and `annotate` offset parameters, considering padding.
    -   Builds the ImageMagick command line arguments as a list.
    -   Executes the `magick` command using `subprocess.run`.
    -   Captures and prints errors if the ImageMagick command fails.
    -   Returns the path of the successfully created watermarked image.

4.  **`watermark_cli/cli.py`**:
    -   Defines the CLI using the `click` library.
    -   The `main` function serves as the entry point for the `watermark` command.
    -   Defines CLI arguments (`path`) and options (`--text`, `--size`, etc.).
    -   Loads configuration using `config.load_config()`.
    -   Merges CLI options with the loaded configuration. CLI options have higher priority. Ensures the watermark text is available.
    -   Determines if the input `path` is a file or directory.
    -   If a file, calls `add_watermark` once.
    -   If a directory, iterates through its top-level contents. For each item that is a file with a recognized image extension and does not already contain the postfix, it calls `add_watermark`.
    -   Prints the output path(s) of the watermarked image(s) or skip messages to the console.

## Program Logic Flow

1.  User executes `watermark <path> [options...]` in the terminal.
2.  Poetry directs the execution to `watermark_cli.cli:main`.
3.  `cli.py`: `main` function starts.
4.  `cli.py`: Calls `config.load_config()` to get configuration settings, merging defaults with `config.json`.
5.  `cli.py`: Parses command-line arguments provided by the user.
6.  `cli.py`: Merges CLI arguments into the configuration dictionary. CLI values override config values.
7.  `cli.py`: Validates that watermark text is present (either from CLI or config). Exits if not.
8.  `cli.py`: Checks if the input `path` points to a file or a directory.
9.  **File Path**:
    -   `cli.py`: Calls `watermark.add_watermark()` with the file path and the final merged options.
    -   `watermark.py`: Constructs the ImageMagick command based on options.
    -   `watermark.py`: Executes the `magick` command via `subprocess`.
    -   `watermark.py`: Returns the output path to `cli.py`.
    -   `cli.py`: Prints the output path.
10. **Directory Path**:
    -   `cli.py`: Iterates through items in the specified directory.
    -   `cli.py`: For each item:
        -   Checks if it is a file with a valid image extension.
        -   Checks if the filename already contains the specified `postfix`.
        -   If it's a valid image file and not already watermarked, calls `watermark.add_watermark()` (steps 9.1 - 9.3).
        -   `cli.py`: Prints the output path for the processed file or a skip message.
11. Program exits.

## External Dependencies

-   **ImageMagick:** The `magick` command-line tool must be installed and accessible in the system's PATH for the core image processing to work. The script relies entirely on invoking this external program.
