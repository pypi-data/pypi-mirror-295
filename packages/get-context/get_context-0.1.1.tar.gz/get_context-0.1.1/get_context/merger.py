# merger.py

# Copyright (c) Aiden R. McCormack. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for more information.

# This file handles the core functionality of the program.

import os
from .directory_structure import write_directory_structure
from .file_utils import is_human_readable, has_valid_extension
from .ignore_utils import load_ignore_patterns, get_ignored_items


def setup_output_file(output_file):
    """Set up the output file by removing the old file if it exists."""
    if os.path.exists(output_file):
        os.remove(output_file)
    return open(output_file, 'w')


def get_ignore_patterns():
    """Get ignore patterns from .contextignore or .gitignore, if available."""
    if os.path.exists(".contextignore"):
        ignore_dir = ".contextignore"
    elif os.path.exists(".gitignore"):
        ignore_dir = ".gitignore"
    else:
        return None, None

    ignore_patterns = load_ignore_patterns(ignore_dir)
    print(f"Using ignore patterns from {ignore_dir} for brevity:")
    print(get_ignored_items(ignore_dir))
    return ignore_patterns, ignore_dir


def exclude_directories(dirs, root, ignore_patterns, exclude_dirs):
    """Modify dirs in-place to exclude directories based on ignore patterns or default list."""
    if ignore_patterns:
        dirs[:] = [d for d in dirs if not ignore_patterns.match_file(os.path.join(root, d))]
    else:
        dirs[:] = [d for d in dirs if d not in exclude_dirs]


def process_file(file_path, directory, outfile):
    """Process an individual file: check readability, write to the output file."""
    relative_path = os.path.relpath(file_path, directory)

    # Check if the file is human-readable
    if is_human_readable(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(f"{relative_path}\n")
                outfile.write(infile.read())
                outfile.write("\n\n" + "=" * 50 + "\n\n")
        except (UnicodeDecodeError, IOError):
            outfile.write(f"{relative_path}\n")
            outfile.write("Text not generated, file is not human-readable or could not be decoded\n\n")
            outfile.write("=" * 50 + "\n\n")
    else:
        outfile.write(f"{relative_path}\n")
        outfile.write("Text not generated, file is not human-readable\n\n")
        outfile.write("=" * 50 + "\n\n")


def merge_files_in_directory(directory, valid_extensions=None, output_file='context.txt'):
    """Main function that orchestrates the merging of files in the directory."""
    # Setup: delete the old output file if it exists and open a new one
    outfile = setup_output_file(output_file)

    # Get ignore patterns, or use default exclusions
    ignore_patterns, ignore_dir = get_ignore_patterns()
    default_exclude_dirs = ['env', 'venv', '__pycache__', '.git', 'build', 'dist']
    exclude_dirs = default_exclude_dirs if ignore_patterns is None else []

    # Write the directory structure at the top of the file
    outfile.write("Directory Structure:\n")
    write_directory_structure(directory, outfile, ignore_patterns=ignore_patterns, exclude_dirs=exclude_dirs)

    outfile.write("\n")
    outfile.write("=" * 50 + "\n\n")

    # Walk through all files and subdirectories
    for root, dirs, files in os.walk(directory):
        exclude_directories(dirs, root, ignore_patterns, exclude_dirs)

        for file in files:
            file_path = os.path.join(root, file)

            # Skip the output file (context.txt) itself
            if file == output_file:
                continue

            # Skip files based on ignore patterns
            if ignore_patterns and ignore_patterns.match_file(file_path):
                continue

            # If valid extensions are provided, only include matching files
            if valid_extensions and not has_valid_extension(file, valid_extensions):
                continue

            # Process the file (read, check human readability, write to output)
            process_file(file_path, directory, outfile)

    # Close the output file after processing
    outfile.close()
    print(f"Generated 'context.txt' at '{os.getcwd()}/context.txt'")
