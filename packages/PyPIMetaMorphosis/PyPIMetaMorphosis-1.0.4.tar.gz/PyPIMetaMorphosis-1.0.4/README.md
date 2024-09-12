# PyPIMetaMorphosis

This project creates a PyPI-ready project structure automatically using Python. It simplifies the process of building and organizing files for Python packages, including setting up a folder structure, creating essential files like `LICENSE`, `README.md`, `.gitignore`, `setup.py`, and initializing directories like `src`, `test`, and `app`.

## Project on PyPI

View the project on PyPI: [PyPIMetaMorphosis](https://pypi.org/project/PyPIMetaMorphosis/)

## Demonstration Video

[![PyPIMetaMorphosis Demonstration](./images/thumbnail2.png)](https://youtu.be/-AcR4Aasgv0)

## Features

- Automatically creates a PyPI project structure
- Generates necessary files such as `setup.py`, `LICENSE`, and `README.md`
- Initializes directories for app, source, and test files
- Customizable for author name, email, project name, and description

## Use Cases

- Ideal for developers who want to quickly set up a Python project for publishing to PyPI.
- Saves time by generating required files and folder structures automatically.
- Suitable for maintaining consistent project formats across multiple Python packages.

## Getting Started

Install the MERNcraft package from PyPI using pip:

```bash
pip install PyPIMetaMorphosis
```

OR

Clone this repository or download the script and run it to create your project structure:

```bash
git clone https://github.com/Hardvan/PyPIMetaMorphosis
cd PyPIMetaMorphosis
python PyPIMetaMorphosis.py
```

## Notes

- Ensure that Python 3.6 or later is installed on your system.
- Customize the setup.py file as per your project's needs.

## Run the following commands to update the package (for maintainers)

1. Change version in `setup.py`
2. Run the following commands

   ```bash
   python setup.py bdist_wheel sdist
   twine check dist/*
   twine upload dist/*
   ```
