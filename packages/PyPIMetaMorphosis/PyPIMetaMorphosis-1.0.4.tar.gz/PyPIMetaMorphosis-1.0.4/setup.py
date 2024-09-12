from setuptools import setup, find_packages

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="PyPIMetaMorphosis",
    version="1.0.4",
    author="Hardik Pawar",
    author_email="hardikpawarh@gmail.com",
    description="Create a ready-to-publish PyPI project structure with the given project name, author name, author email, and project description.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hardvan/PyPIMetaMorphosis",
    keywords=["automation", "pypi", "template", "project",
              "structure", "skeleton", "repository"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
