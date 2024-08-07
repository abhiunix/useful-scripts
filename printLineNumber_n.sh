#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage: $0 <line-number> <file>"
  exit 1
fi

LINE_NUMBER=$1
FILE=$2

sed -n "${LINE_NUMBER}p" "$FILE"

# usage:
# cp printLineNumber_n.sh printLineNumber_n
# cp printLineNumber_n /usr/local/bin/ 
# chmod +x /usr/local/bin/printLineNumber_n
# line 3 printLineNumber_n.sh
# the above command will print the line number 3 of printLineNumber_n.sh file.
