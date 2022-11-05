#!/bin/bash

snake_to_camel() {
    IFS= read -r -d $'\0' str
    if hash perl 2>/dev/null; then
        echo $str | perl -nE 'say lcfirst join "", map {ucfirst lc} split /[^[:alnum:]]+/'
    else
        echo $str | sed -r 's/(.)_+(.)/\1\U\2/g;s/^[a-z]/\U&/'
    fi
}

echo "$1" | snake_to_camel
