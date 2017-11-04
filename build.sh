#!/bin/bash

python3.6 -m venv thinglang-env
source thinglang-env/bin/activate
pip install -r requirements.txt

mkdir /app-src/build
cd /app-src/build
cmake ..
make
make test
/app-src/build/thinglang --version

export PATH=$PATH:/app-src/build/thinglang/
export PYTHONPATH=/app-src

cd /app-src
pytest tests/
