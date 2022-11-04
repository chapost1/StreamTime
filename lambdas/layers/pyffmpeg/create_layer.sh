#!/bin/bash

# make script workdir relative
cd $(dirname "$0")
service="pyffmpeg lambda layer"
../../../common/is_new_build_needed.sh "$service" $(pwd) "no_directory" "./Dockerfile" "ffmpeg-python-layer-factory:latest" "source" "dummy_exclude" &
pid1=$!
wait $pid1
is_new_build_needed=$?

if [[ "$is_new_build_needed" -eq 42 ]]; then
    echo "building $service..."
    # build image
    docker build -t ffmpeg-python-layer-factory:latest .
    # prepare output dir
    rm -rf $(pwd)/source
    mkdir $(pwd)/source
    # cp output from image
    docker run --rm -it -v $(pwd)/source:/source ffmpeg-python-layer-factory cp /var/task/python.zip /source
elif [[ $is_new_build_needed -eq 0 ]]; then
    echo "no new build needed for $service"
else
    echo "$service: unexpected error during is_new_build_needed detection"
    exit 1;
fi



