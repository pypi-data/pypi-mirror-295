from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    page_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="cli-intern",
    version="0.0.1",
    author="jonasaacampos",
    author_email="jonasaacampos@gmail.com",
    description="A collection of utilities for command-line interfaces (CLIs) in Python.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonasaacampos/cli_utils",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.0",
)