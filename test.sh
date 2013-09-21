#!/usr/bin/env bash

INPUT=entrada/*
OUTPUT=saida/*


# Create folder
mkdir testoutput/

for f in $INPUT
do
    # Extract filename from path
    fname=`basename $f`

    # Execute pythonesque on test case
    python pythonesque.py $f testoutput/tested-$fname

    # Compare output with sample
    out=`diff testoutput/tested-$fname saida/$fname`

    if [ -n "$out" ] 
    then
        # Error
        echo "Error on $fname..."
    else
        echo "$fname OK"
    fi
done

# Remove previous folder
rm -rf testoutput/
