# -*- coding: utf-8 -*-
"""

Contact: lukas.kontenis@lightcon.com, support@lightcon.com

Copyright (c) 2019-2023 Light Conversion
All rights reserved.
www.lightcon.com
"""
import setuptools
import codecs
import os.path

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fr:
    install_requires = [line.strip() for line in fr.readlines()]

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setuptools.setup(
    name="harpiamm",
    version=get_version("harpiamm/__init__.py"),
    author="Lukas Kontenis",
    author_email="lukas.kontenis@lightcon.com",
    description="A Python library for the HARPIA microscopy module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/lukaskontenis/harpiamm/",
    packages=setuptools.find_packages(include=["harpiamm*"]),
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
            'Documentation': 'https://lightconupdater.blob.core.windows.net/documentation/lightcon/index.html'},
    python_requires='>=3.6',
    data_files=[
        ('scripts')]
)
