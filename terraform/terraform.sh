#!/bin/bash

Help() {
   # Display Help
   echo "Syntax: ./terraform.sh [OPTIONS...]"
   echo
   echo "Options:"
   echo "h     Print this Help."
   echo "c     COMMAND            (plan|apply|destroy)"
   echo "a     AWS ACCESS_KEY     (required)"
   echo "s     AWS SECRET_KEY     (required)"
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

while getopts ":hc:a:s:r" option; do
   case $option in
      h) # display Help
         Help;;
      c)
         command=$OPTARG;;
      a)
         access_key=$OPTARG;;
      s)
         secret_key=$OPTARG;;
      \?) # Invalid option
         echo "Error: Invalid option"
         Help;;
   esac
done

# required
if [ -z "$command" ]
then
    echo "command option is required"
    Help
fi
if [ -z "$access_key" ]
then
    echo "access_key option is required"
    Help
fi
if [ -z "$secret_key" ]
then
    echo "secret_key option is required"
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

   # run command
   terraform $command -var="aws_access_key=$access_key" -var="aws_secret_key=$secret_key"
else
   echo "invalid command"
   Help
fi
