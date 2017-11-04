#!/bin/bash

python3.6 -m venv thinglang-env
source thinglang-env/bin/activate
pip install -r requirements.txt

mkdir /app-src/build
cd /app-src/build
cmake ..
make

export PATH=$PATH:/app-src/build/thinglang/:/app-src/build/tests/
export PYTHONPATH=/app-src


thinglang --version
ctest --verbose

cd /app-src
pytest tests/
