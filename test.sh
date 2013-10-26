#!/usr/bin/env bash

INPUT=Arquivos_teste/arquivos_com_1_erro/entrada/*

# Remove previous folder
rm -rf testoutput/

# Create folder
mkdir testoutput/

for f in $INPUT
do
    # Extract filename from path
    fname=`basename $f`

    # Execute pythonesque on test case
    python pythonesque.py $f testoutput/tested-$fname

    # Compare output with sample
    out=`diff testoutput/tested-$fname Arquivos_teste/arquivos_com_1_erro/saida/$fname`

    if [ -n "$out" ] 
    then
        # Error
        echo "Error on $fname..."
        echo ""
    else
        echo "$fname OK"
        echo ""
    fi
done

