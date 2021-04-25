#!/bin/sh
set -ex

./clean.sh
./env/bin/pip install build
./env/bin/python -m build

ls -la ./dist
