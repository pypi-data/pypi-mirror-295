# directory_structure.py

# Copyright (c) Aiden R. McCormack. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for more information.

# this file handles the logic for printing the directory structure at the top of the context file.

import os

def write_directory_structure(directory, outfile, indent_level=0, ignore_patterns=None, exclude_dirs=None):
    """Recursively write the directory structure to the output file."""
    indent = '\t' * indent_level  # Indentation for the current level
    
    # Write the current directory name at the top level
    if indent_level == 0:
        top_level_dir = os.path.basename(os.path.abspath(directory))
        outfile.write(f"{top_level_dir}/\n")

    # List contents of the directory
    try:
        items = sorted(os.listdir(directory))  # Sort to ensure consistent ordering
    except OSError as e:
        outfile.write(f"{indent}Error accessing directory: {e}\n")
        return

    for item in items:
        item_path = os.path.join(directory, item)

        # Check if the item is a directory or file
        if os.path.isdir(item_path):
            # Check if this directory should be excluded
            relative_item_path = os.path.relpath(item_path, os.path.dirname(directory))
            if should_exclude(relative_item_path, ignore_patterns, exclude_dirs):
                outfile.write(f"{indent}\t{item}/ (contents omitted)\n")
            else:
                outfile.write(f"{indent}\t{item}/\n")
                # Recursively call the function for subdirectories
                write_directory_structure(item_path, outfile, indent_level + 1, ignore_patterns, exclude_dirs)
        else:
            # It's a file, just write it
            outfile.write(f"{indent}\t{item}\n")


def should_exclude(relative_path, ignore_patterns, exclude_dirs):
    """Determine if a directory or file should be excluded based on ignore patterns."""
    normalized_path = relative_path + "/" if os.path.isdir(relative_path) else relative_path
    return (ignore_patterns and ignore_patterns.match_file(normalized_path)) or (
        exclude_dirs and any(ex_dir in normalized_path for ex_dir in exclude_dirs)
    )
