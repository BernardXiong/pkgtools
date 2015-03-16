#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $(basename $0) </path/to/Pkgfile>"
    exit 1
fi

declare -A cfields
cfields=([description]="Description" [maintainer]="Maintainer" [url]="URL" [depends]="Depends on")

for k in "${!cfields[@]}"; do
    v="${cfields[$k]}"
    export "$k"="$(egrep "#\s*${v}\:" $1 | sed -E "s/#\s*${v}\:\s*(.*)\s*/\1/")"
done

export PATH=""

exec /bin/bash --noprofile --norc -r << EOF
source $1

print_var() {
    if [ -n "\$2" ]; then
        echo -e "\$1: \${2//\'/\\\\\'}"
    else
        echo "\$1:"
    fi
}

print_array() {
    key=\$1; shift
    if [ -n "\$1" ]; then
        array=( "\$@" )
        echo "\$key:"
        for i in \${array[@]}; do
            echo "  - \$i"
        done
    else
        echo "\$key:"
    fi
}

print_var   name        "\$name"
print_var   version     "\$version"
print_var   release     "\$release"
print_var   description "\$description"
print_var   url         "\$url"
print_array groups      "\${groups[@]}"
print_array depends     "\${depends[@]}"
print_array makedepends "\${makedepends[@]}"
print_array provides    "\${provides[@]}"
print_array conflicts   "\${conflicts[@]}"
print_array replaces    "\${replaces[@]}"
print_array source      "\${source[@]}"
EOF
