#!/bin/bash

mkdir /app-src/build
cd /app-src/build
cmake ..
make
/app-src/build/thinglang --build-only