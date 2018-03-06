#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: Put package requirements here
]

setup_requirements = [
    # TODO(MarcoFavorito): Put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: Put package test requirements here
]

setup(
    name='pythogic',
    version='0.2.5',
    description="Python package for deal with logical formulas and formal systems",
    long_description=readme + '\n\n' + history,
    author="Marco Favorito",
    author_email='marco.favorito@gmail.com',
    url='https://github.com/MarcoFavorito/pythogic',
    packages=find_packages(include=['pythogic*']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pythogic',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
