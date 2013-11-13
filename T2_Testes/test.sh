#!/usr/bin/env bash

INPUT1=Arquivos_teste/arquivos_com_1_erro/entrada/*

# Remove previous folder
rm -rf testoutput/

# Create folder
mkdir testoutput/
mkdir testoutput/arquivos_com_1_erro/

for f in $INPUT1
do
    # Extract filename from path
    fname=`basename $f`

    # Execute pythonesque on test case
    python pythonesque.py $f testoutput/arquivos_com_1_erro/tested-$fname

    # Compare output with sample
    out=`diff testoutput/arquivos_com_1_erro/tested-$fname Arquivos_teste/arquivos_com_1_erro/saida/$fname`

    if [ -n "$out" ] 
    then
        # Error
        echo "Error on $fname..."
    else
        echo "$fname OK"
    fi
done

INPUT2=Arquivos_teste/arquivos_sem_erros/entrada/*

# Create folder
mkdir testoutput/arquivos_sem_erros/

for f in $INPUT2
do
    # Extract filename from path
    fname=`basename $f`

    # Execute pythonesque on test case
    python pythonesque.py $f testoutput/arquivos_sem_erros/tested-$fname

    # Compare output with sample
    out=`diff testoutput/arquivos_sem_erros/tested-$fname Arquivos_teste/arquivos_sem_erros/saida/$fname`

    if [ -n "$out" ] 
    then
        # Error
        echo "Error on $fname..."
    else
        echo "$fname OK"
    fi
done
