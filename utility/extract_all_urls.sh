#!/bin/bash

# call with path to one or more .md files, e.g.
# ./utility/extract_all_urls.sh ../content/NewcomersGuide/Chapter*/*/*/*.md

grep --extended-regexp --word-regexp --only-matching --ignore-case --no-filename 'https?://[^ ]+' "$@" \
| sort \
| uniq -ui
