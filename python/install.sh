#!/bin/bash

# Install the Python package
if [ $(which python | wc -l) -ne 0 ]; then
   echo "Installing library for Python 2"
   python setup.py install --record python2_files.txt
fi

echo

if [ $(which python3 | wc -l) -ne 0 ]; then
   echo "Installing library for Python 3"
   python3 setup.py install --record python3_files.txt
fi

echo

echo "uldaq Python API install complete."
