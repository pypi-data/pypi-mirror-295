# GET CONTEXT

## About
**Get Context** is a directory context generator designed to provide a structured overview of the contents of a directory and its subdirectories. It generates a single text file that lists the directory structure and the contents of text or program files, while excluding non-human-readable files such as binary or multimedia files. This tool is particularly useful for organizing and reviewing large codebases or data directories. It can also
be used to easily pass the contents of a directory to a large language AI model for further analysis.

## Installation and Usage
This program is available as the Python package "get_context". If Python is installed on your system, you should be able to run:

```
pip install get_context
```
After the package is installed, the program can be run on the command line by typing:

```
get_context <directory> [file_extensions...]
```

The program takes the directory as the first argument and can optionally filter files by specified extensions. For example:

```
get_context . .py .txt
```

This will generate a text file containing the directory structure and the contents of `.py` and `.txt` files within the specified directory.

## Disclaimer
This program is still in development and is currently buggy. Further testing and implementation is required before it can be used as a
fully-fledged, reliable product. **For this reason, it is currently unavailable as a pip package.** 

## Attributions
This program uses both Python’s built-in libraries and external libraries for various functionalities:

* **File and Directory Handling:** The program uses Python’s built-in `os` and `mimetypes` libraries for file and directory manipulation.
* **Text Encoding and Decoding:** The program uses Python's built-in `codecs` and `io` libraries to handle different text encodings.
* **Pattern Matching:** The program uses the external `pathspec` library to handle file exclusion patterns, specifically for interpreting and applying `.gitignore`-style patterns.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
