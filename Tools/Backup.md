Mongodump

Limitations:

![Uploading image.png…]()

Common options:

     --out
     --db
     --collection
     --readPreference
     --gzip
     --archive
     --oplog


 Backup dump structure example:

       dump
      ├── easternSalesDatabase
      │    ├── sales.bson
      │    ├── sales.metadata.json
      │    └── salesByMonthView.metadata.json
      ├── westernSalesDatabase
      │    ├── sales.bson
      │    ├── sales.metadata.json
      │    └── salesByMonthView.metadata.json
      └── oplog.bson


Use mongodump with a Collection

    mongodump  --db=test --collection=records

Use mongodump with a Database and Exclude Specified Collections

    mongodump  --db=test --excludeCollection=users --excludeCollection=salaries

Use mongodump with Access Control

    mongodump --host=mongodb1.example.net --port=37017 --username=user --authenticationDatabase=admin --out=/opt/backup/mongodump-2011-10-24

To compress the archive file output by mongodump, use the --gzip option in conjunction with the --archive option, specifying the name of the compressed file.

    mongodump --archive=test.20150715.gz --gzip --db=test



**Copy and Clone Databases**

For example, to copy the test database from a local instance running on the default port 27017 to the examples database on the same instance, you can:

    mongodump --archive="mongodump-test-db" --db=test

Use mongorestore with --nsFrom and --nsTo to restore (with database name change) from the archive:

    mongorestore --archive="mongodump-test-db" --nsFrom="test.*" --nsTo="examples.*"



To create a consistent mongodump backup file using oplog entries, use the mongodump --oplog option. To restore data from the backup file, use the mongorestore --oplogReplay option.
