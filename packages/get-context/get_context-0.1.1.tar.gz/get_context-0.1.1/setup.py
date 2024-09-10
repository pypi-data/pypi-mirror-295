# setup.py

# Copyright (c) Aiden R. McCormack. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for more information.

# This file keeps track of the metadata for the package.

from setuptools import setup, find_packages

# Read the requirements from requirements.txt
def read_requirements():
    with open('requirements.txt') as req_file:
        return req_file.read().splitlines()

setup(

    # Package information
    name='get_context',  # the name of the package
    version='0.1.1',  # the current version
    description='Generates a single text document for a directory',  # short description
    
    # Read the contents of your README.md file for a full-length description
    long_description=open('README.md').read(),  # file should be opened and read
    long_description_content_type='text/markdown',  # specifies that the long description is markdown

    # URL to the source code or documentation
    url='https://github.com/Aiden2244/get-context',  # source code location

    # Classifiers: help others find the package based on metadata
    classifiers=[
        'Programming Language :: Python :: 3',  # specifies Python 3
        'License :: OSI Approved :: MIT License',  # your chosen license
        'Operating System :: OS Independent',  # works on any OS
    ],

    # Author information
    author='Aiden R. McCormack',  # your name
    author_email='aidenm2244@proton.me',  # your email
    
    # Entry point: where the program starts executing
    entry_points={
        'console_scripts': [
            'get_context=get_context.cli:main',  # links command to main function
        ],
    },

    # Packages: automatically discovers all modules and packages
    packages=find_packages(),  # finds all Python packages recursively in the project

    # Dependencies: external libraries your project needs (empty here)
    install_requires=read_requirements(),

    # Additional metadata (optional, you can add if needed)
    include_package_data=True,  # include non-Python files like README.md
)

