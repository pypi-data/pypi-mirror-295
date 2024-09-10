# file_utils.py

# Copyright (c) Aiden R. McCormack. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for more information.

# This file handles logic for determining if files are human-readable and have valid extensions.


import mimetypes

def is_human_readable(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        return mime_type.startswith('text') or 'application/javascript' in mime_type or 'application/xml' in mime_type
    return False

def has_valid_extension(file_name, valid_extensions):
    return any(file_name.endswith(ext) for ext in valid_extensions)
