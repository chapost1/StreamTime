#!/bin/bash

non_alpha_to_underscores() {
    IFS= read -r -d $'\0' str
    echo $str | sed -E 's/[^[:alnum:][:space:]]+/_/g'
}

snake_to_upper() {
    IFS= read -r -d $'\0' str
    if hash perl 2>/dev/null; then
        echo $str | perl -nE 'say lcfirst join "", map {ucfirst lc} split /[^[:alnum:]]+/'
    else
        echo $str | sed -r 's/(.)_+(.)/\1\U\2/g;s/^[a-z]/\U&/'
    fi
}

echo "$1" | non_alpha_to_underscores | snake_to_upper
