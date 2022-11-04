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

if cmp --silent -- code_md5sum.txt.new code_md5sum.txt; then
    echo "no new build needed for ui"
else
    echo "building ui..."
    cd ./code
    ng build
    cd ..
fi

mv code_md5sum.txt.new code_md5sum.txt
