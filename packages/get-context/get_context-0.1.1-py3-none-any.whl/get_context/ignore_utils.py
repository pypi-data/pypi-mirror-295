# ignore_utils.py

# Copyright (c) Aiden R. McCormack. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for more information.

# This file handles logic for loading ignore patterns

import os
import pathspec

def load_ignore_patterns(filename='.contextignore'):
    """Load ignore patterns from .contextignore (or .gitignore, if present)."""
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            patterns = file.read().splitlines()
        patterns = [line for line in patterns if line.strip() and not line.strip().startswith('#')]
        return pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, patterns)
    return None


def get_ignored_items(file_path):
    """
    Reads a file and returns a list of lines that begin with a letter or a '.' or '_' character.
    Other lines are ignored.
    """
    if not os.path.exists(file_path):
        return []

    ignored_items = []
    
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            # Check if the line starts with a letter or '.' and ignore comments or empty lines
            if stripped_line and (stripped_line[0].isalpha() or stripped_line[0] == '.' or stripped_line[0] == "_"):
                ignored_items.append(stripped_line)
    
    return ignored_items
