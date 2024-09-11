#!/usr/bin/env python3
"""Keyt setup."""

from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = fh.read()

requirements = ["pyperclip", "base58"]

setup(
    name="keyt",
    version="1.2.0",
    author="keyt",
    author_email="",
    description="Stateless password manager and generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT license",
    url="https://github.com/deoktr/keyt",
    project_urls={
        "Bug Tracker": "https://github.com/deoktr/keyt/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
    ],
    packages=find_packages(include=["keyt", "keyt.*"]),
    python_requires=">=3.5",
    entry_points={
        "console_scripts": [
            "keyt=keyt.cli:cli",
        ],
    },
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)
