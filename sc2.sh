#!/bin/bash


# Define the input file
INFILE=/opt/dblist.txt

# Read the input file line by line
while read -r LINE
do
    printf '%s\n' "$LINE" >> /coll_size.log
        mongo $LINE --host 179.31.1.44 --eval "db.sampleColl.totalSize()" >> /output.log
done < "$INFILE"
