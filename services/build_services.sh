#!/bin/bash

# make script workdir relative
cd $(dirname "$0")

# validate docker daemon is running
if (! docker ps 2>&1>/dev/null); then
    echo "Docker is not running. Please start docker on your computer"
    exit 1;
fi


# execute all build scripts
find . -type f -name build.sh -exec sh -c '
  for file do
    if ! sh $file; then
      echo 1 > ./build_errors.txt
      kill -s PIPE "$PPID"
      exit 1
    fi
  done' sh {} +;


if [ -f ./build_errors.txt ]; then
    rm -rf ./build_errors.txt
    exit 1;
fi

rm -rf ./build_errors.txt
exit 0;
