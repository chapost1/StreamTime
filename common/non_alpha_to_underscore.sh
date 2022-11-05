#!/bin/bash

spaces_to_underscores() {
    IFS= read -r -d $'\0' str
    echo ${str// /_}
}

non_alpha_to_underscore() {
    IFS= read -r -d $'\0' str
    echo $str | sed -E 's/[^[:alnum:][:space:]]+/_/g'
}

echo "$1" | spaces_to_underscores | non_alpha_to_underscore
