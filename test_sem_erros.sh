#!/usr/bin/env bash

INPUT=Arquivos_teste/2.arquivos_gera_codigo_C/1.entrada/*
INPUTC=(Arquivos_teste/2.arquivos_gera_codigo_C/3.entrada_execucao/*)
OUTPUTC=(Arquivos_teste/2.arquivos_gera_codigo_C/4.saida/*)

# Remove previous folder
rm -rf testoutput/

# Create folder
mkdir testoutput/

for f in $INPUT
do
    # Extract filename from path
    fname=`basename $f`

    # Execute pythonesque on test case
    python pythonesque.py $f testoutput/$fname.c

done

    # Grab every output to compile in C
    TESTOUT=testoutput/*.c
for f2 in $TESTOUT 
do
    gcc $f2 -o  ${f2%.c}.r
done

    TESTOUT=(testoutput/*.r)
for ((i = 0; i < ${#INPUTC[@]}; i++)) 
do
    in=${INPUTC[i]}
    out=${TESTOUT[i]}.txt

    ${TESTOUT[i]} < $in > $out

    out=`diff $out ${OUTPUTC[i]}`

    # Compare output with sample
    if [ -n "$out" ] 
    then
        # Error
        echo "Error on ${TESTOUT%.r}..."
    else
        echo "${TESTOUT%.r} OK"
    fi
done
