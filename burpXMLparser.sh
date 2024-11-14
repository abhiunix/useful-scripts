#!/bin/bash
cat extracted.xml | grep "<request base64=" | awk -F'[' '{print $3}' | awk -F']]' '{print $1}' | tee allRequestsInBase64.txt >/dev/null

file=allRequestsInBase64.txt

if [ -e ./requests-from-extractedxml/ ]; then 
echo "requests-from-extractedxml File exists."
    else
    mkdir requests-from-extractedxml 
fi

counter=1

for i in `cat $file`
do
    echo $i | base64 -d | tee ./requests-from-extractedxml/$counter.txt
    echo ""
    echo ""
    let counter++
        
done

rm allRequestsInBase64.txt
