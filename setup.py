#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import codecs
import os

# Get the long description from the relevant file
with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
main_pkg = "py2casefold"
setup(
    name=main_pkg,
    version=open("VERSION", "r").read().strip(),
    description="Unicode casefold support for python 2.",
    long_description=long_description,
    url='https://github.com/rwarren/py2casefold',
    author='Russell Warren',
    author_email='russ@perspexis.com',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        "Operating System :: OS Independent",
    ],
    keywords='unicode casefold',
    packages=[], # no sub-packages... just one function, really!
    install_requires = [],
    package_data={},
    py_modules=["py2casefold", ],
    data_files=["VERSION", "LICENSE", "CaseFolding.txt"],
    entry_points={},
)
