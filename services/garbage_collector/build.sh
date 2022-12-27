#!/bin/bash

# make script workdir relative
cd $(dirname "$0")
service="garbage_collector"
../../common/is_new_build_needed.sh "$service" $(pwd) "./source/" "./source/Dockerfile" "stream-time-garbage-collector:latest" "source" "*/venv/*" &
pid1=$!
wait $pid1
is_new_build_needed=$?

if [[ "$is_new_build_needed" -eq 42 ]]; then
    echo "building $service..."

    cd ./source

    docker build -t stream-time-garbage-collector:latest . &
    pid2=$!
    wait $pid2
    is_docker_build_succeeded=$?
    if [[ "$is_docker_build_succeeded" -eq 0 ]]; then
        exit 0;
    else
        echo "$service docker build failed";
        exit 1;
    fi
elif [[ $is_new_build_needed -eq 0 ]]; then
    echo "no new build needed for $service"
else
    echo "$service: unexpected error during is_new_build_needed detection"
    exit 1
fi
