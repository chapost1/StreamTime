#!/bin/bash

# make script workdir relative
cd $(dirname "$0")

# execute all create_layer scripts
find . -name create_layer.sh -exec bash {} \;
