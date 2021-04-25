#!/bin/sh
set -ex

./clean.sh
./build_dist.sh
./env/bin/pip install twine
./env/bin/python -m twine upload dist/*
