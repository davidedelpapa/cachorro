"""Main setup for the library."""
from setuptools import setup, find_packages
from cachorro import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=VERSION,
    version="0.0.1",
    author="Davide Del Papa",
    author_email="davidedelpapa((at))gmail.com",
    description="A simple function caching library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidedelpapa/cachorro",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
