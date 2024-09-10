from setuptools import setup, find_packages

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="FileHarvestor",
    version="1.0.3",
    author="Hardik Pawar",
    author_email="hardikpawarh@gmail.com",
    description="FileHarvestor is a Python utility that reads the contents of specified files and writes them to both text and markdown files. If a file does not exist, it is added to a list of not found files. This tool is useful for consolidating and documenting the contents of multiple files in a directory.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hardvan/FileHarvestor",
    keywords=["file", "harvestor", "read", "write",
              "text", "markdown", "file-reader", "read-file"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
