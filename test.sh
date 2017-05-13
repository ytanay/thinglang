#! /bin/bash

RED='\033[0;31m' # Red
BB='\033[0;34m'  # Blue
NC='\033[0m' # No Color
BG='\033[0;32m' # Green

error() { >&2 echo -e "${RED}$1${NC}"; }
showinfo() { echo -e "${BG}$1${NC}"; }
success() { echo -e "${BB}$1${NC}"; }
alert () { echo -e "${RED}$1${NC}"; }

pwd
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Debug ../thingc
make -j8


if [ $? -ne 0 ]; then
    error "Error: there were compilation errors!"
	# Terminate script and outputs 3
    exit 3
fi

success "All done."