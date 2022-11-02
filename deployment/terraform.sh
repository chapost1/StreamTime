#!/bin/bash

Help() {
   # Display Help
   echo "Syntax: ./terraform.sh [OPTIONS...]"
   echo
   echo "Options:"
   echo "-h | --help              Print this Help."
   echo "--command                (plan|apply|destroy)           (required)"
   echo "--aws_access_key         AWS ACCESS_KEY                 (required)"
   echo "--aws_secret_key         AWS SECRET_KEY                 (required)"
   echo
   exit 1;
}

is_valid_command() {
    local valid=( destroy apply plan )
    local value=$1
    for elem in "${valid[@]}"; do
        [[ $value == $elem ]] && return 0
    done
    return 1
}

error()
{
    echo "$arg0: $*" >&2
    exit 1
}

# validate user has terraform
if hash terraform 2>/dev/null; then
    echo "terraform seems to be installed, proceeding..."
else
    echo "terraform is not installed, exiting..."
    exit 1;
fi

# validate user has aws cli
if hash aws 2>/dev/null; then
    echo "aws cli seems to be installed, proceeding..."
else
    echo "aws cli is not installed, exiting..."
fi

args=()

while test $# -gt 0; do
        case $1 in
        -h|--help) Help;;
        --command) command=$2; shift;;
        --aws_access_key) aws_access_key=$2; shift;;
        --aws_secret_key) aws_secret_key=$2; shift;;
        *) args+=($1);;
        esac
        shift
done

set -- "${args[@]}"

# required
if [ -z "$command" ]
then
    echo "command option is required"
    Help
fi
if [ -z "$aws_access_key" ]
then
    echo "aws_access_key option is required"
    Help
fi
if [ -z "$aws_secret_key" ]
then
    echo "aws_secret_key option is required"
    Help
fi

# make sure script workdir is relative to terraform directory
cd $(dirname "$0")

if is_valid_command "$command"; then
   if [ $command = "destroy" ]; then
       echo "no builds are necessary for destroy command."
   else
      echo "checking for necessery builds..."
      # run necessary builds

      # lambda layars
      ../lambdas/layers/build_layers.sh

      # packages
      echo "no packages to build yet"
   fi

   aws configure set aws_access_key_id $aws_access_key
   aws configure set aws_secret_access_key $aws_secret_key

   # run command
   terraform $command -var="aws_access_key=$aws_access_key" -var="aws_secret_key=$aws_secret_key"
else
   echo "invalid command"
   Help
fi
