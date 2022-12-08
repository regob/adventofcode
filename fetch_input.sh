#!/bin/bash

if [ -z "$2" ]; then
    YEAR=2022
else
    YEAR=$2
fi

if [ -z "$1" ]; then
    echo "Day param not provided."
    exit 1
else
    DAY=$1
fi

URL=https://adventofcode.com/${YEAR}/day/${DAY}/input
COOKIE=$(cat cookie.txt)
FILE="inputs/${YEAR}_${DAY}.txt"
wget -O $FILE --header="Cookie: ${COOKIE}" "$URL"
N_LINES=$(wc -l $FILE | cut -d ' ' -f1)
echo "Num lines: $N_LINES"
echo "Sample:"
head -n 10 $FILE