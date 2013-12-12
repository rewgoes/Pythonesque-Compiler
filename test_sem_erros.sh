#!/usr/bin/env bash

INPUT=Arquivos_teste/2.arquivos_gera_codigo_C/1.entrada/*
INPUTC=Arquivos_teste/2.arquivos_gera_codigo_C/3.entrada_execucao/
OUTPUTC=Arquivos_teste/2.arquivos_gera_codigo_C/4.saida/


# Remove previous folder
rm -rf testoutput_C/
rm -rf testoutput/

# Create folder
mkdir testoutput_C/
mkdir testoutput/

for f in $INPUT
do
    # Extract filename from path
    fname=`basename $f`

    # Execute pythonesque on test case
    python pythonesque.py $f testoutput_C/$fname.c

    # Compile in C
    gcc testoutput_C/$fname.c -o testoutput_C/$fname

	testoutput_C/$fname < $INPUTC$fname > testoutput/$fname
	
	# Compare output with sample
    out=`diff -b -B testoutput/$fname $OUTPUTC$fname`

    if [ -n "$out" ] 
    then
        # Error
        echo "Error on $fname..."
    else
        echo "$fname OK"
    fi

done
