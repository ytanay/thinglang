#!/bin/bash -e

python3.6 -m venv thinglang-build-env
source thinglang-build-env/bin/activate
pip install wheel
pip install -r requirements.txt