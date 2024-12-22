#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <domain>"
    exit 1
fi

# Store the argument (domain) in a variable
domain="$1"

# Execute the pipeline
waybackurls "$domain" | \
    tac | \
    sed "s#\\\\/#/#g" | \
    egrep -o "src['\"]?[=: ]?[^'\"]+.js[^'\"> ]*" | \
    awk -F '/' '{if(length($2))print "https://"$2}' | \
    sort -fu | \
    xargs -I '%' sh -c "curl -k -s \"%\"" | \
    sed "s/[;}\)>]/\n/g" | \
    grep -Po "(['\"])(https?:)?//[^'\"]+|(\.(get|post|ajax|load)\s*\(['\"](https?:)?//[^'\"]+)" | \
    awk -F "['\"]" '{print $2}' | \
    sort -fu

