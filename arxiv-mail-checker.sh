#!/bin/bash

PYTHON=python3
WD=$DEV/arxiv-mail-checker

EDITOR=TextEdit
OUTPUT=$WD/results-$(/bin/date +%Y-%m-%d-%H-%M).txt
KEYWORDS=$WD/keywords.txt
AUTHORS=$WD/authors.txt
LOGIN=$WD/login.txt

$PYTHON $WD/arxivmailchecker.py --login $LOGIN --keywords-file $KEYWORDS \
                                --authors-file $AUTHORS --output $OUTPUT
if [ "$1" == "--open" ]; then
    open -a $EDITOR $OUTPUT
fi
