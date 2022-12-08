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
wget -O "inputs/${YEAR}_${DAY}.txt" --header="Cookie: ${COOKIE}" "$URL"
