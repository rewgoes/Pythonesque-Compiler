#!/bin/bash

# Get Array of files
infiles=(entrada/*)
outfiles=(saida/*)

# Choose a random number
rn=$((RANDOM % ${#infiles[@]}))

# Choose a file that matches that number
in=${infiles[$rn]}
out=${outfiles[$rn]}

# Output testing file
printf "Testing file: %s\n" "$in"
# Test file and output result 
diff <(python pythonesque.py $in) $out
