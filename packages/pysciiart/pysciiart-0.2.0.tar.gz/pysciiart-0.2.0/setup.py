#!/usr/bin/env python3
from setuptools import setup

from src.pysciiart import __version__


def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


def parse_requirements(filename):
    """ Load requirements from a requirements file """
    with open(filename, 'r') as f:
        return [line.strip() for line in f
                if not line.startswith('#')]


setup(
    name='pysciiart',
    version=__version__,
    packages=['pysciiart'],
    package_dir={'pysciiart': './src/pysciiart'},
    test_suite='tests',
    setup_requires=['pytest-runner'],
    install_requires=parse_requirements('requirements.txt'),
    tests_require=['pytest'],
    url='https://gitlab.com/alcibiade/pysciiart',
    license='MIT',
    author='Yannick Kirschhoffer',
    author_email='alcibiade@alcibiade.org',
    description='A set of python libraries used to generate ASCII art from high level data structures.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
)
