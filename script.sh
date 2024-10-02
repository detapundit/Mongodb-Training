#!/bin/bash

#Backup path
BACKUPS_DIR="/opt/backup"

# Define the input file
INFILE=/root/dblist.txt

# Read the input file line by line
while read -r LINE
do
    printf '%s\n' "$LINE" >> /coll_backup.log 
  mongodump --db $LINE --collection collname --gzip --out $BACKUPS_DIR
done < "$INFILE"
