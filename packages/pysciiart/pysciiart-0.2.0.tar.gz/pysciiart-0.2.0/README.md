[![PyPI version](https://badge.fury.io/py/pysciiart.svg)](https://badge.fury.io/py/pysciiart)

# pysciiart

A set of python scripts to generate ascii art models.

## Requirements

* termcolor

## Install

You can install this library from PyPI:

```
alcibiade@mobydick:~$ sudo pip3 install pysciiart
```

## Deployment of a new version

* Update revision in src/pysciiart/__init__.py
* Commit and tag with corresponding version number
* Build distribution: python setup.py sdist
* Upload distribution to PyPI: twine upload dist/*
