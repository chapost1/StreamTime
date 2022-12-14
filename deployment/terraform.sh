#!/bin/bash

Help() {
    # Display Help
    echo "Syntax: ./terraform.sh [OPTIONS...]"
    echo
    echo "Options:"
    echo "-h | --help              Print this Help."
    echo "--command                Resources provisioning         (plan|apply|destroy)         (required)"
    echo "--aws_access_key         AWS ACCESS_KEY                 (AWS ACCESS_KEY)             (required)"
    echo "--aws_secret_key         AWS SECRET_KEY                 (AWS SECRET_KEY)             (required)"
    echo "--app_name               App Name                       (any unique name)            (required)"
    echo "--domain                 Registered Route53 Domain      (any approved domain)        (required)"
    echo "--db_mode                DDL operation on RDS           (init|patch|none)            (default is none)"
    echo
    exit 1
}

is_valid_command() {
    local valid=(destroy apply plan)
    local value=$1
    for elem in "${valid[@]}"; do
        [[ $value == $elem ]] && return 0
    done
    return 1
}

is_valid_db_mode() {
    local valid=(init patch none)
    local value=$1
    for elem in "${valid[@]}"; do
        [[ $value == $elem ]] && return 0
    done
    return 1
}

error() {
    echo "$arg0: $*" >&2
    exit 1
}

# validate user has docker
if hash docker 2>/dev/null; then
    echo "docker seems to be installed, proceeding..."
    # validate docker daemon is running
    if (! docker ps 2>&1>/dev/null); then
        echo "Docker is not running. Please start docker on your computer";
        exit 1;
    fi
else
    echo "docker is not installed, exiting..."
    exit 1
fi

# validate user has terraform
if hash terraform 2>/dev/null; then
    echo "terraform seems to be installed, proceeding..."
else
    echo "terraform is not installed, exiting..."
    exit 1
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
    -h | --help) Help ;;
    --command)
        command=$2
        shift
        ;;
    --aws_access_key)
        aws_access_key=$2
        shift
        ;;
    --aws_secret_key)
        aws_secret_key=$2
        shift
        ;;
    --app_name)
        app_name=$2
        shift
        ;;
    --domain)
        domain=$2
        shift
        ;;
    --db_mode)
        db_mode=$2
        shift
        ;;
    *) args+=($1) ;;
    esac
    shift
done

set -- "${args[@]}"

# required
if [ -z "$command" ]; then
    echo "command option is required"
    Help
fi
if [ -z "$aws_access_key" ]; then
    echo "aws_access_key option is required"
    Help
fi
if [ -z "$aws_secret_key" ]; then
    echo "aws_secret_key option is required"
    Help
fi
if [ -z "$app_name" ]; then
    echo "app_name option is required"
    Help
fi
if [ -z "$domain" ]; then
    echo "domain option is required"
    Help
fi

# has default
if [ -z "$db_mode" ]; then
    echo "db_mode is none"
    db_mode=none
fi

# make sure script workdir is relative to terraform directory
cd $(dirname "$0")

# normalize app_name (no special/whitespcaes)
# snake case for easier next step transform to camel case for db name
snake_case_app_name=$($(pwd)/../common/non_alpha_to_underscore.sh "$app_name")
# most of resources requires dash in name (and not underscore), thus, normalize snake case to use dashse
normalized_app_name=$($(pwd)/../common/underscore_to_hypen.sh "$snake_case_app_name")

# create DB name
db_name=$($(pwd)/../common/snake_to_camel_case.sh "$snake_case_app_name")DB

if is_valid_command "$command"; then
    if is_valid_db_mode "$db_mode"; then
        # handle db_init cache buster
        if [ $db_mode = "init" ]; then
            echo Are you sure you want to init DB? It will reset all of your data! "(Y or N)"
            read x
            # now check if $x is "y"
            if [[ "$x" =~ ^[Yy]$ ]]; then
                echo $(date +%s) >./modules/rds/ddl/init_id.txt
            else
                echo "command has been canceled"
                exit 1
            fi
        fi
        # handle db_patch cache buster
        if [ $db_mode = "patch" ]; then
            echo Are you sure you want to patch DB? "(Y or N)"
            read x
            # now check if $x is "y"
            if [[ "$x" =~ ^[Yy]$ ]]; then
                echo $(date +%s) >./modules/rds/ddl/patch_id.txt
            else
                echo "command has been canceled"
                exit 1
            fi
        fi
        # if not destroy, build source code
        if [ $command = "destroy" ]; then
            echo "no builds are necessary for destroy command."
        else
            echo "checking for necessery builds..."
            # run necessary builds

            # lambda layars
            ../lambdas/layers/build_layers.sh &
            pid1=$!
            wait $pid1
            is_build_failed=$?
            if [[ "$is_build_failed" -eq 1 ]]; then
                echo "failed to build lambda layers";
                exit 1;
            fi
            # services
            ../services/build_services.sh &
            pid2=$!
            wait $pid2
            is_build_failed=$?
            if [[ "$is_build_failed" -eq 1 ]]; then
                echo "failed to build services";
                exit 1;
            fi

        fi

        aws configure set aws_access_key_id $aws_access_key
        aws configure set aws_secret_access_key $aws_secret_key
        # run command
        terraform $command -var="aws_access_key=$aws_access_key" -var="aws_secret_key=$aws_secret_key" \
            -var="app_name=$normalized_app_name" -var="domain=$domain" -var="db_name=$db_name"
    else
        echo "invalid db_mode"
        Help
    fi
else
    echo "invalid command"
    Help
fi
