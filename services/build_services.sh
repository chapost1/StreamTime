#!/bin/bash

# make script workdir relative
cd $(dirname "$0")

# execute all build scripts
find . -name build.sh -exec bash {} \;
