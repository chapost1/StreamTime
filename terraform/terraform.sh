#!/bin/bash

Help() {
   # Display Help
   echo "Syntax: ./terraform.sh [OPTIONS...]"
   echo
   echo "Options:"
   echo "-h | --help               Print this Help."
   echo "--command                (plan|apply|destroy)           (required)"
   echo "--aws_access_key         AWS ACCESS_KEY                 (required)"
   echo "--aws_secret_key         AWS SECRET_KEY                 (required)"
   echo "--pg_host                Postgres Host                  (required)"
   echo "--pg_port                Postgres Port                  (default: 6739)"
   echo "--pg_user                Postgres Username              (required)"
   echo "--pg_pass                Postgres Password              (required)"
   echo "--pg_db                  Postgres Database Name         (required)"
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

args=()

while test $# -gt 0; do
        case $1 in
        -h|--help) Help;;
        --command) command=$2; shift;;
        --aws_access_key) aws_access_key=$2; shift;;
        --aws_secret_key) aws_secret_key=$2; shift;;
        --pg_host) pg_host=$2; shift;;
        --pg_port) pg_port=$2; shift;;
        --pg_user) pg_user=$2; shift;;
        --pg_pass) pg_pass=$2; shift;;
        --pg_db) pg_db=$2; shift;;
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
if [ -z "$pg_host" ]
then
    echo "pg_host option is required"
    Help
fi
if [ -z "$pg_user" ]
then
    echo "pg_user option is required"
    Help
fi
if [ -z "$pg_pass" ]
then
    echo "pg_pass option is required"
    Help
fi
if [ -z "$pg_db" ]
then
    echo "pg_db option is required"
    Help
fi
# defaults
if [ -z "$pg_port" ]
then
    pg_port=6739
    echo "no pg_port has been specified, using default: $pg_port"
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

   # run command
   terraform $command -var="aws_access_key=$aws_access_key" -var="aws_secret_key=$aws_secret_key" \
                      -var="pg_host=$pg_host" -var="pg_port=$pg_port" \
                      -var="pg_user=$pg_user" -var="pg_pass=$pg_pass" \
                      -var="pg_db=$pg_db"
else
   echo "invalid command"
   Help
fi
