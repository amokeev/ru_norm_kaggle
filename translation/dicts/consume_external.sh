#!/usr/bin/env bash

#Takes external data and generates dictionary


#The script expects everything required be installed
#If it fails - check the error and add what's missing.
#Make sure there are no spaces in paths and names
#You need Amazon x1.16xlarge to run this. Or alternative with 512+Gb of memory and 50-100 CPUs

set -e
DATA="https://storage.googleapis.com/text-normalization/ru_with_types.tgz"
date
wget ${DATA}
mkdir data
cd data
tar -xzvf ../ru_with_types.tgz
cd ru_with_types

export DATASETS=""
for sfile in `ls output*`;do
    export DATASETS="${DATASETS} ${sfile}.csv"
    python3 ../../external2competition_ru.py ${sfile} ${sfile}.csv &
done

echo "Awaited datasets: ${DATASETS}"
FAIL=0
for job in `jobs -p`; do
    wait $job || let "FAIL+=1"
done

echo "FAILED dataset generations: $FAIL"

ls -l ${DATASETS}

for dsfile in ${DATASETS};do
    python3 ../../build_dictionary.py ${dsfile} ${dsfile}.dict &
done

echo Waiting for dictionaries
FAIL=0
for job in `jobs -p`; do
    wait $job || let "FAIL+=1"
done

echo "FAILED dictionaries: $FAIL"

#This is not 100% correct - there can be keys with different values.
cat *.dict  > ../RussianExternalDictionary.csv
sort -u ../RussianExternalDictionary.csv >RussianExternalDictionary1.csv

gzip ../RussianExternalDictionary1.csv

echo Done. data/RussianExternalDictionary1.csv.gz is ready to be copied out
date