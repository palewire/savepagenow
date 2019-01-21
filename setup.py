#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='savepagenow',
    version='0.0.13',
    description='A simple Python wrapper for archive.org\'s "Save Page Now" capturing service',
    long_description=read('README.rst'),
    author='Ben Welsh',
    author_email='ben.welsh@gmail.com',
    url='http://www.github.com/pastpages/savepagenow/',
    packages=('savepagenow',),
    include_package_data=True,
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'six',
        'requests>=2.20.0',
        'click',
    ],
entry_points='''
        [console_scripts]
        savepagenow=savepagenow.api:cli
    ''',
)
