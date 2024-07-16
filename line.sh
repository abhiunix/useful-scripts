#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage: $0 <line-number> <file>"
  exit 1
fi

LINE_NUMBER=$1
FILE=$2

sed -n "${LINE_NUMBER}p" "$FILE"

# usage:
# cp line.sh line
# cp line /usr/local/bin/ 
# chmod +x /usr/local/bin/line
# line 3 line.sh
# the above command will print the line number 3 of line.sh file.
