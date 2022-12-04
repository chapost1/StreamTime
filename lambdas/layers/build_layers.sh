#!/bin/bash

# make script workdir relative
cd $(dirname "$0")

# validate docker daemon is running
if (! docker ps 2>&1>/dev/null); then
    echo "Docker is not running. Please start docker on your computer"
    exit 1;
fi


# execute all create_layer scripts
find . -type f -name create_layer.sh -exec sh -c '
  for file do
    if ! sh $file; then
      echo 1 >> ./layers_creation_errors.txt
      kill -s PIPE "$PPID"
      exit 1
    fi
  done' sh {} +;


if [ -f ./layers_creation_errors.txt ]; then
    rm -rf ./layers_creation_errors.txt
    exit 1;
fi

rm -rf ./layers_creation_errors.txt
exit 0;