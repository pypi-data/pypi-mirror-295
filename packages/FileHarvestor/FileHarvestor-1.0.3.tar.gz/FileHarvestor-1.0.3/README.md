# FileHarvestor

This script is a Python utility that reads the contents of specified files and writes them to both text and markdown files. If a file does not exist, it is added to a list of not found files. This tool is useful for consolidating and documenting the contents of multiple files in a directory.

## FileHarvestor on PyPI

View the package on PyPI: [FileHarvestor](https://pypi.org/project/FileHarvestor/)

## Demonstration Video

[![FileHarvestor Demonstration](./demo/thumbnail2.png)](https://youtu.be/9wgHg_YINWo?si=q4RWUkmS1w9ic5Vl)

## Features

- Reads the contents of specified files.
- Writes the contents to both a text file (`contents.txt`) and a markdown file (`contents.md`).
- Handles non-existent files and maintains a list of files that were not found.
- Provides a summary of the process, including read times for each file and overall execution time.

## How it works

1. The script takes a list of file paths as input and iterates through each file.
2. For each file, it checks if it exists, reads its contents, and writes the contents to both a text file and a markdown file.
3. If a file is not found, it is added to a list of not found files.
4. The script provides detailed output about the success or failure of reading each file and summarizes the overall process at the end.

Function arguments:

- **file_list (list, optional):** List of files to read. Defaults to None.
- **output_text_file (str, optional):** Output text file. Defaults to './output/contents.txt'.
- **output_markdown_file (str, optional):** Output markdown file. Defaults to './output/contents.md'.

## Usage

1. Install the `FileHarvestor` package from PyPI using pip:

   ```bash
   pip install FileHarvestor
   ```

   OR

   Clone or download the `FileHarvestor.py` script to your local machine.

   ```bash
   git clone https://github.com/Hardvan/FileHarvestor
   cd FileHarvestor
   pip install .
   ```

2. Call the `read_files_in_directory` function from the `FileHarvestor` package with the directory path as an argument.

   ```python
   from FileHarvestor import read_files_in_directory

   read_files(file_list=['./path/to/file1.txt', './path/to/file2.txt'], output_text_file='./output/contents.txt', output_markdown_file='./output/contents.md')
   ```

   View the `run.py` file for an example of how to use the `FileHarvestor` package.

## Run the following commands to update the package (for maintainers)

1. Change version in `setup.py`
2. Run the following commands

   ```bash
   python setup.py bdist_wheel sdist
   twine check dist/*
   twine upload dist/*
   ```
