#!/bin/bash

CHECKER=./arxivmailchecker.py
PYTHON=python3
EDITOR=TextEdit
OUTPUT=results-$(date +%Y-%m-%d-%H-%M).txt
KEYWORDS=keywords.txt
AUTHORS=authors.txt
LOGIN=login.txt

$PYTHON $CHECKER --login $LOGIN --keywords $KEYWORDS --authors $AUTHORS \
                 --output $OUTPUT \
              && open -a $EDITOR $OUTPUT 
