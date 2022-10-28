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
   echo "r     AWS_REGION         (us-east-1 as default)"
   echo
   exit 1;
}

while getopts ":hc:a:s:r" option; do
   case $option in
      h) # display Help
         Help;;
      c) # Enter a name
         command=$OPTARG;;
      a) # Enter a name
         access_key=$OPTARG;;
      s) # Enter a name
         secret_key=$OPTARG;;
      r) # Enter a name
         region=$OPTARG;;
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
# has defaults
if [ -z "$region" ]
then
    region=us-east-1
    echo "region is not set, default=$region"
fi

terraform $command -var="aws_access_key=$access_key" -var="aws_secret_key=$secret_key" -var="aws_region=$region"
