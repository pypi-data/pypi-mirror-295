"""
    Module: setup.py
    Author: Neethukrishnan P
    
    Description:
    
    License:
    
    Created on: 08-29-2024
"""
from setuptools import setup, find_packages
from os import path

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="e2e_testing_framework",
    version="0.1",
    packages=find_packages(),
    description="testing platform for unittest test cases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Neethukrishnan P",
    license="MIT",
    install_requires=[
        "requests",
        "fastapi",
        "pytest"
    ],
)

