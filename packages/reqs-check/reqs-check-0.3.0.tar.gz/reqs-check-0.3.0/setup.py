from setuptools import setup, find_packages

setup(
    name="reqs-check",
    version="0.3.0",
    author="Brice Fotzo",
    author_email="bricef.tech@gmail.com",
    description="A tool to check and compare dependencies(requirements.txt and so on) files for Python projects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bricefotzo/reqs-check",
    packages=find_packages(),
    install_requires=["pandas", "tabulate", "termcolor", "typer"],
    entry_points={
        "console_scripts": [
            "reqs-check=reqs_check.main:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
