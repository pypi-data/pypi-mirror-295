#!/bin/bash

#python3 -m pip install --upgrade pip
#python3 -m pip install --upgrade twine
#python3 -m pip install --upgrade pkginfo

rm -rf dist
mkdir dist
python -m build
ls dist -l
python3 -m twine upload dist/*
