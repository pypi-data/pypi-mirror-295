# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="punicalab_core",
    version="0.1.0",
    author="punicalab",
    author_email="duzgun.ilaslan@punicalab.com",
    description="A Python SDK for managing Status ENUMs and utilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/punicaLab-fuzeAI/punicalab_core",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
