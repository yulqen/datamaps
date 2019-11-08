#!/usr/bin/env python

from setuptools import find_packages, setup

import datamaps

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='datamaps',
    version=datamaps.__version__,
    description='Collect and clean data using Excel spreadsheets.',
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Text Processing",
    ],
    keywords='data console commandline excel',
    author='Matthew Lemon',
    author_email='matt@matthewlemon.com',
    maintainer='Matthew Lemon',
    maintainer_email='matt@matthewlemon.com',
    url='https://github.com/hammerheadlemon/datamaps',
    packages=find_packages(),
    python_requires='>=3.6',
    entry_points={'console_scripts': [
        'datamaps = datamaps.main:cli'
    ]},
    setup_requires=['wheel'],
    install_requires=[
        'click',
        'python-dateutil',
        'bcompiler-engine'
    ],
    test_suite='datamaps.tests')
