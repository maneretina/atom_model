#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
from os.path import join, dirname
import atom_model
setup(
	name='atom_model',
	version='1.0',
	packages=find_packages(),
	include_package_data=True,
	test_suite='tests',
	install_requires=['numpy', 'pandas'],
	long_description = open(join(dirname(__file__), 'README.md')).read(),
)
