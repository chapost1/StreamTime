#!/bin/bash

service=$1
workdir=$2
direcory_to_lookup=$3
dockerfile_to_cmp=$4
docker_image=$5
build_folder_name=$6
exlude_path_lookup=$7

# make script workdir relative
cd $workdir

md5_directory() {
    if hash md5sum 2>/dev/null; then
        find $@ -type f -not -path "$exlude_path_lookup" -exec md5sum {} + | md5sum
    elif hash md5 2>/dev/null; then
        find $@ -type f -not -path "$exlude_path_lookup" -exec md5 {} + | md5
    fi
}

BUILD=false

if [ $direcory_to_lookup = "no_dockerfile" ]; then
    echo "$service does not have a Dockerfile to lookup"
else
    # need to lookup Dockerfile and compare hash
    md5_directory $direcory_to_lookup >dockerfile_md5sum.txt.new
    if [ ! -f dockerfile_md5sum.txt ]; then
        touch dockerfile_md5sum.txt
    fi

    # check if md5 identical
    if cmp --silent -- dockerfile_md5sum.txt.new dockerfile_md5sum.txt; then
        echo "$service Dockerfile md5 is identical"
    else
        echo "$service Dockerfile has been changed"
        BUILD=true
    fi
    mv dockerfile_md5sum.txt.new dockerfile_md5sum.txt
fi

if [ $direcory_to_lookup = "no_directory" ]; then
    echo "$service does not have a directory to lookup"
else
    # need to lookup directory and compare hash
    md5_directory $direcory_to_lookup >code_md5sum.txt.new
    if [ ! -f code_md5sum.txt ]; then
        touch code_md5sum.txt
    fi

    # check if md5 identical
    if cmp --silent -- code_md5sum.txt.new code_md5sum.txt; then
        echo "$service source code md5 is identical"
    else
        echo "$service source code has been changed"
        BUILD=true
    fi
    mv code_md5sum.txt.new code_md5sum.txt
fi

# detect if image exists
if [[ "$(docker images -q $docker_image 2> /dev/null)" == "" ]]; then
    echo "$service docker image ($docker_image) does not exist"
    BUILD=true
fi
# detect no dist folder
if [ ! -d "$(pwd)/$build_folder_name" ]
then
    echo "$service $build_folder_name, build folder is missing" 
    BUILD=true
fi

if [ $BUILD = "false" ]; then
    exit 0;
else
    exit 42;
fi
