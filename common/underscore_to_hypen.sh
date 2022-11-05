#!/bin/bash

underscore_to_hypen() {
    IFS= read -r -d $'\0' str
    echo "$str" | tr '_' '-'
}

echo "$1" | underscore_to_hypen
