#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cnspy_csv2dataframe',
    version="0.2.3",
    author='Roland Jung',
    author_email='roland.jung@aau.at',    
    description='CSV to pandas.Dataframe converter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/aau-cns/cnspy_csv2dataframe/',
    project_urls={
        "Bug Tracker": "https://github.com/aau-cns/cnspy_csv2dataframe/issues",
    },    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    
    packages=find_packages(exclude=["test_*", "TODO*"]),
    python_requires='>=3.6',
    install_requires=['numpy', 'pandas', 'cnspy_numpy_utils', 'cnspy_spatial_csv_formats'],
)
