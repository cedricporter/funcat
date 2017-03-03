#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#

from os.path import dirname, join
from setuptools import (
    find_packages,
    setup,
)

from pip.req import parse_requirements


with open(join(dirname(__file__), 'funcat/VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='funcat',
    version=version,
    description='funcat',
    packages=find_packages(exclude=[]),
    author='Hua Liang',
    url='https://github.com/cedricporter/funcat',
    author_email='et@everet.org',
    package_data={'': ['*.*']},
    install_requires=[str(ir.req) for ir in parse_requirements("requirements.txt", session=False)],
    zip_safe=False,
)
