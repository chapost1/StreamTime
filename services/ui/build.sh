#!/bin/bash

# make script workdir relative
cd $(dirname "$0")
service="ui"
../../common/is_new_build_needed.sh "$service" $(pwd) "./code/" "./Dockerfile" "ng-frontend-dist:latest" "dist" "*/node_modules/*" &
pid1=$!
wait $pid1
is_new_build_needed=$?

if [[ "$is_new_build_needed" -eq 42 ]]; then
    echo "building $service..."

    docker build -t ng-frontend-dist:latest . &
    pid2=$!
    wait $pid2
    is_docker_build_succeeded=$?
    if [[ "$is_docker_build_succeeded" -eq 0 ]]; then
        # prepare output dir
        rm -rf $(pwd)/dist
        mkdir $(pwd)/dist
        # cp output from image
        docker run --rm -t -v $(pwd)/dist:/tmp/dist ng-frontend-dist mv /var/ng /tmp/dist
        mv $(pwd)/dist/ng/* $(pwd)/dist/
        rm -rf $(pwd)/dist/ng

        exit 0;
    else
        echo "$service docker build failed";
        exit 1;
    fi
elif [[ $is_new_build_needed -eq 0 ]]; then
    echo "no new build needed for $service"
else
    echo "$service: unexpected error during is_new_build_needed detection"
    exit 1;
fi
