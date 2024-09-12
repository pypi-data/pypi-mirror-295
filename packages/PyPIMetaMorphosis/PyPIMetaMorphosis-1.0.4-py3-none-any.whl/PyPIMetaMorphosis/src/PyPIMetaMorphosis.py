import os
import time


def _get_user_choice(prompt):
    """Get user choice (y/n) and return True if 'y' and False if 'n'.

    Args
    ----
    - prompt (str): Prompt message.

    Returns
    -------
    - bool: True if 'y' and False if 'n'.
    """
    while True:
        try:
            print(prompt, end='')
            choice = input().lower()
            if choice in ['y', 'n']:
                return choice == 'y'
            raise ValueError
        except ValueError:
            print("Invalid input. Please enter 'y' or 'n'.")


def create_pypi_project(root_dir=os.getcwd(),
                        project_name=None,
                        author_name=None, author_email=None, project_desc=None):
    """
    Create a ready-to-publish PyPI project structure with the given project name, author name, author email, and project description.

    Args
    ----
    - root_dir (str, optional): Root directory to create the project structure. Defaults to os.getcwd().
    - project_name (str): Name of the project.
    - author_name (str, optional): Author name. Defaults to None.
    - author_email (str, optional): Author email. Defaults to None.
    - project_desc (str, optional): Project description. Defaults to None.

    Steps
    -----
    1. Change to root directory
    2. Create top-level files: LICENSE, README.md, .gitignore, run.py, setup.py
    3. Create app folder & files
    4. Create Project folder inside app
    5. Create src directory and files
    6. Create test directory and files
    7. Print success message and time taken

    Raises
    ------
    - ValueError: If project name is not provided.
    """

    # Check for required inputs
    if not project_name:
        raise ValueError("Project name is required!")

    start_time = time.time()

    # Step 1: Change to root directory
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
        print(f"📂 Created directory {root_dir}")
    os.chdir(root_dir)
    print(f"📂 Changed directory to {root_dir}")

    # Step 2: Create top-level files: LICENSE, README.md, .gitignore, run.py, setup.py
    # LICENSE file
    license_content = f'''MIT License

Copyright (c) 2024 {author_name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
    if os.path.exists("LICENSE"):
        if not _get_user_choice("LICENSE file already exists. Do you want to overwrite it? (y/n): "):
            print("❌ Skipped creating LICENSE file")
        else:
            with open("LICENSE", "w") as f:
                f.write(license_content)
            print("✅ Overwritten LICENSE file")
    else:
        with open("LICENSE", "w") as f:
            f.write(license_content)
        print("✅ Created LICENSE file")
    # README.md file
    readme_content = f'''# {project_name}

## Project on PyPI

## Demonstration Video

## Features

## Use Cases

## Getting Started

Install the {project_name} package from PyPI using pip:

```bash
pip install {project_name}
```

OR

Clone this repository or download the script and run it to create your project structure:

```bash
git clone your_project_url  # TODO: Add your project's GitHub URL
cd {project_name}
python {project_name}.py
```

## Notes

## Run the following commands to update the package (for maintainers)

1. Change version in `setup.py`
2. Run the following commands

   ```bash
   python setup.py bdist_wheel sdist
   twine check dist/*
   twine upload dist/*
   ```
'''
    if os.path.exists("README.md"):
        if not _get_user_choice("README.md file already exists. Do you want to overwrite it? (y/n): "):
            print("❌ Skipped creating README.md file")
        else:
            with open("README.md", "w") as f:
                f.write(readme_content)
            print("✅ Overwritten README.md file")
    else:
        with open("README.md", "w") as f:
            f.write(readme_content)
        print("✅ Created README.md file")
    # .gitignore file
    gitignore_content = '''__pycache__/
.env
build/
'''
    if os.path.exists(".gitignore"):
        if not _get_user_choice(".gitignore file already exists. Do you want to overwrite it? (y/n): "):
            print("❌ Skipped creating .gitignore file")
        else:
            with open(".gitignore", "w") as f:
                f.write(gitignore_content)
            print("✅ Overwritten .gitignore file")
    else:
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore file")
    # run.py file
    runpy_content = f'''import {project_name}

if __name__ == "__main__":
    {project_name}.your_project_method  # TODO: Change this method
'''
    if os.path.exists("run.py"):
        if not _get_user_choice("run.py file already exists. Do you want to overwrite it? (y/n): "):
            print("❌ Skipped creating run.py file")
        else:
            with open("run.py", "w") as f:
                f.write(runpy_content)
            print("✅ Overwritten run.py file")
    else:
        with open("run.py", "w") as f:
            f.write(runpy_content)
        print("✅ Created run.py file")
    # setup.py file
    setup_content = f'''from setuptools import setup, find_packages

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="{project_name}",
    version="1.0.1",
    author="{author_name if author_name else '# TODO'}",
    author_email="{author_email if author_email else '# TODO'}",
    description="{project_desc if project_desc else '# TODO'}",
    package_dir={{"": "app"}},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",  # TODO: Add project URL
    keywords=["example", "pypi", "template"],  # TODO: Add keywords
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
'''
    if os.path.exists("setup.py"):
        if not _get_user_choice("setup.py file already exists. Do you want to overwrite it? (y/n): "):
            print("❌ Skipped creating setup.py file")
        else:
            with open("setup.py", "w") as f:
                f.write(setup_content)
            print("✅ Overwritten setup.py file")
    else:
        with open("setup.py", "w") as f:
            f.write(setup_content)
        print("✅ Created setup.py file")

    # Step 3: Create app folder & files
    os.makedirs("app", exist_ok=True)
    os.chdir("app")
    # README.md inside app
    app_readme_content = f'''# {project_name}

## Project on GitHub

## Features

## Use Cases

## Getting Started

Install the {project_name} package from PyPI using pip:

```bash
pip install {project_name}
```

OR

Clone this repository or download the script and run it to create your project structure:

```bash
git clone your_project_url  # TODO: Add your project's GitHub URL
cd {project_name}
python {project_name}.py
```

## Notes
'''
    if os.path.exists("README.md"):
        if not _get_user_choice("README.md file already exists. Do you want to overwrite it? (y/n): "):
            print("❌ Skipped creating README.md in app folder")
        else:
            with open("README.md", "w") as f:
                f.write(app_readme_content)
            print("✅ Overwritten README.md in app folder")
    else:
        with open("README.md", "w") as f:
            f.write(app_readme_content)
        print("✅ Created README.md in app folder")
    # __init__.py inside app
    with open("__init__.py", "w") as f:
        pass  # Empty file
    print("✅ Created empty __init__.py in app folder")

    # Project folder inside app
    os.makedirs(f"{project_name}", exist_ok=True)
    os.chdir(f"{project_name}")
    # __init__.py inside Project folder
    init_content = f"from .src.{project_name} import your_project_method  # TODO: Change this\n"
    if os.path.exists("__init__.py"):
        if not _get_user_choice("__init__.py file already exists. Do you want to overwrite it? (y/n): "):
            print("❌ Skipped creating __init__.py inside Project folder")
        else:
            with open("__init__.py", "w") as f:
                f.write(init_content)
            print(f"✅ Overwritten __init__.py inside {project_name} folder")
    else:
        with open("__init__.py", "w") as f:
            f.write(init_content)
        print(f"✅ Created __init__.py inside {project_name} folder")

    # Create src directory and files
    os.makedirs("src", exist_ok=True)
    os.chdir("src")
    # __init__.py inside src
    with open("__init__.py", "w") as f:
        pass  # Empty file
    print("✅ Created empty __init__.py in src folder")
    # ProjectName.py inside src
    project_content = f'''def your_project_method():
    print('Hello from {project_name}!\n')  # TODO: Implement this method
'''
    if os.path.exists(f"{project_name}.py"):
        if not _get_user_choice(f"{project_name}.py file already exists. Do you want to overwrite it? (y/n): "):
            print("❌ Skipped creating {project_name}.py in src folder")
        else:
            with open(f"{project_name}.py", "w") as f:
                f.write(project_content)
            print(f"✅ Overwritten {project_name}.py in src folder")
    else:
        with open(f"{project_name}.py", "w") as f:
            f.write(project_content)
        print(f"✅ Created {project_name}.py in src folder")

    # Create test directory and files
    os.chdir("..")
    os.makedirs("test", exist_ok=True)
    os.chdir("test")
    # __init__.py inside test
    with open("__init__.py", "w") as f:
        pass  # Empty file
    print("✅ Created empty __init__.py in test folder")
    # test_ProjectName.py
    test_content = f"import {project_name}\n\n# Write your test cases here\n"
    if os.path.exists(f"test_{project_name}.py"):
        if not _get_user_choice(f"test_{project_name}.py file already exists. Do you want to overwrite it? (y/n): "):
            print("❌ Skipped creating test_{project_name}.py in test folder")
        else:
            with open(f"test_{project_name}.py", "w") as f:
                f.write(test_content)
            print(f"✅ Overwritten test_{project_name}.py in test folder")
    else:
        with open(f"test_{project_name}.py", "w") as f:
            f.write(test_content)
        print(f"✅ Created test_{project_name}.py in test folder")

    end_time = time.time()

    print(f"🎉 PyPI project {project_name} structure created successfully!")
    print(f"⏰ Time taken: {(end_time - start_time) * 1000:.2f} ms")


# Example Usage
if __name__ == "__main__":
    create_pypi_project(root_dir="trial_project",
                        project_name="PyPIMetaMorphosis")
