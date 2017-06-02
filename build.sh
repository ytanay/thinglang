#!/bin/bash

python3.6 -m venv thinglang-env
source thinglang-env/bin/activate
pip install -r requirements.txt

mkdir /app-src/build
cd /app-src/build
cmake ..
make
/app-src/build/thinglang --build-only

cd /app-src
pytest tests/integration