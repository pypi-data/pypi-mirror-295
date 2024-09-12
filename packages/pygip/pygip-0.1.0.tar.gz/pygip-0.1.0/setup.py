import os
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    install_requires=requirements,
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ]
)
