Mongorestore
https://www.mongodb.com/docs/database-tools/mongorestore/mongorestore-examples/

    mongorestore \
     -v \
     --gzip \
     --archive=backup.gz \
     --drop \
     "mongodb+srv://dbaTestAdmin@cluster1.xwgj1.mongodb.net"


The following options can be used with the mongorestore command. Check out the MongoDB documentation for more information.

     --nsInclude
     --nsExclude
     --drop
     --noIndexRestore
     --writeConcern
     --gzip
     --archive
     --oplogReplay


    mongorestore --host=mongodb1.example.net --port=27017 --username=user --authenticationDatabase=admin /opt/backup/mongodump-2011-10-24
    
    mongorestore --nsInclude=test.purchaseorders dump/
    
    mongorestore --db=test --collection=purchaseorders dump/test/purchaseorders.bson
    
    mongorestore --nsInclude='transactions.*' --nsExclude='transactions.*_dev' dump/
    
    mongorestore --nsInclude="data.*" --nsFrom="data.$prefix$_$customer$" --nsTo="$customer$.$prefix$"

