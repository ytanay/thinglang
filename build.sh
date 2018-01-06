#!/bin/bash -e

source thinglang-build-env/bin/activate

mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=Release ..
make VERBOSE=1

cd ..
python3.6 setup.py install

