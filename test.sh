#!/bin/bash -e

source thinglang-build-env/bin/activate

thinglang --version

pytest tests/

export PATH=$PATH:/opt/thinglang/build/tests/
cd build
ctest --verbose