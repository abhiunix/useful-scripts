#!/bin/bash

cat $1 | grep "<request base64=" | awk -F'[' '{print $3}' | awk -F']]' '{print $1}' | tee allRequestsInBase64.txt >/dev/null

file=allRequestsInBase64.txt
if [ -e ./requests-from-extractedxml/ ]; then 
    echo "requests-from-extractedxml directory exists."
else
    mkdir requests-from-extractedxml 
fi

counter=1

for i in `cat $file`
do
    decoded_request=$(echo $i | base64 -d)
    echo "$decoded_request" > ./requests-from-extractedxml/$counter.txt
    echo ""
    echo ""
    let counter++
done

for file in ./requests-from-extractedxml/*.txt
do
    if grep -q "^OPTIONS " "$file"; then
        echo "Removing $file as it contains an OPTIONS request."
        rm "$file"
    fi
done

counter=1
for file in ./requests-from-extractedxml/*.txt
do
    mv "$file" ./requests-from-extractedxml/$counter.txt
    let counter++
done

rm allRequestsInBase64.txt
