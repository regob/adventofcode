#!/bin/bash

if [ -z "$2" ]; then
    YEAR=$(date +"%Y")
else
    YEAR=$2
fi

if [ -z "$1" ]; then
    DAY=$(date +"%d")
else
    DAY=$(printf "%02d" "$1")
fi

echo "Fetching input for $DAY Dec $YEAR..."

DAY_NOLEADINGZERO=$(echo "$DAY" | sed 's/^0*//')
URL=https://adventofcode.com/${YEAR}/day/${DAY_NOLEADINGZERO}/input
FILE="input/${YEAR}_${DAY}.txt"

wget -O $FILE --load-cookies=./cookies.txt "$URL"
N_LINES=$(wc -l $FILE | cut -d ' ' -f1)
echo "Num lines: $N_LINES"
echo "Sample:"
head -n 10 $FILE
