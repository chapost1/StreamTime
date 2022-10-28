#!/bin/bash

# relative workdir
cd $(dirname "$0")
# build image
docker build -t pillow-python-layer-factory:latest .
# prepare output dir
rm -rf $(pwd)/source
mkdir $(pwd)/source
# cp output from image
docker run --rm -it -v $(pwd)/source:/source pillow-python-layer-factory cp /var/task/python.zip /source
