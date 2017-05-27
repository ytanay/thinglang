#!/bin/bash

mkdir /app-src/thingc/build
cd /app-src/thingc/build
cmake ..
make
cp * /app-src/build-output