#!/usr/bin/env bash

INPUT=Arquivos_teste/1.arquivos_com_erros/entrada/*

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
    out=`diff testoutput/tested-$fname Arquivos_teste/1.arquivos_com_erros/saida/$fname`

    if [ -n "$out" ] 
    then
        # Error
        echo "Error on $fname..."
    else
        echo "$fname OK"
    fi
done

