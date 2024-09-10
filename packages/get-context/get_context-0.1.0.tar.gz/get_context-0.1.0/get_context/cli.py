# cli.py

# Copyright (c) Aiden R. McCormack. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for more information.

# This file handles the CLI logic for the context generator.

import sys
import os
from .merger import merge_files_in_directory

def print_usage():
    print("Usage:")
    print("  get_context <directory> [file_extensions...]")
    print("Description:")
    print("  This program processes all human-readable files in the given directory and its subdirectories.")
    print("  Optionally, you can specify file extensions to filter which files to include.")
    print("Examples:")
    print("  get_context .         # Process all human-readable files.")
    print("  get_context . .py .txt  # Process only .py and .txt files.")

def main():
    if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
        print("Error: Invalid CLI arguments")
        print_usage()
        sys.exit(1)

    print(f"Generating context file for directory {sys.argv[1]}")
    directory = sys.argv[1]
    if len(sys.argv) > 2:
        extensions = sys.argv[2:]
        if all(ext.startswith('.') for ext in extensions):
            print(f"Reading only files with extensions {extensions}")
            merge_files_in_directory(directory, valid_extensions=extensions)
        else:
            print("Error: Invalid CLI arguments")
            print_usage()
            sys.exit(1)
    else:
        merge_files_in_directory(directory)
