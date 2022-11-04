#!/bin/bash

# make script workdir relative
cd $(dirname "$0")

md5_directory() {
    if hash md5sum 2>/dev/null; then
        find $@ -type f -not -path '*/node_modules/*' -exec md5sum {} + | md5sum
    elif hash md5 2>/dev/null; then
        find $@ -type f -not -path '*/node_modules/*' -exec md5 {} + | md5
    fi
}

md5_directory ./code/ >code_md5sum.txt.new
if [ ! -f code_md5sum.txt ]; then
    touch code_md5sum.txt
fi

if cmp --silent -- code_md5sum.txt.new code_md5sum.txt; then
    echo "no new build needed for ui"
else
    echo "building ui..."

    docker build -t ng-frontend-dist:latest .
    # prepare output dir
    rm -rf $(pwd)/dist
    mkdir $(pwd)/dist
    # cp output from image
    docker run --rm -it -v $(pwd)/dist:/tmp/dist ng-frontend-dist mv /var/ng /tmp/dist
    mv $(pwd)/dist/ng/* $(pwd)/dist/
    rm -rf $(pwd)/dist/ng
fi

mv code_md5sum.txt.new code_md5sum.txt
