Mongoimport

     mongoimport \
     -v \
     --collection newCollection \
     --type json \
     --mode insert \
     --drop \
     --file export.json \
     "mongodb+srv://dbaTestAdmin@cluster1.xwgj1.mongodb.net/test”


     --db
     --collection
     --type
     --mode
     --upsertFields
     --drop
     --file

    mongoimport -c=people -d=example --mode=upsert --file=people-20160927.json
    mongoimport -c=people -d=example --mode=merge --file=people-20160927.json
    mongoimport -c=people -d=example --mode=delete --file=people-20160927.json

CSV Import

    mongoimport --db=users --collection=contacts --type=csv --headerline --file=/opt/backups/contacts.csv

file name as coll. name

    mongoimport --db=users --type=csv --headerline --file=/opt/backups/contacts.csv
