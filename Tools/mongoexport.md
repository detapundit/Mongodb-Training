Mongoexport


     --collection
     --type
     --out
     --jsonFormat
     --query

--jsonFormat=<canonical|relaxed>
Default: relaxed

Modifies the output to use either canonical or relaxed mode of the MongoDB Extended JSON (v2) format.

For differences between canonical and relaxed modes, see MongoDB Extended JSON (v2).

     mongoexport \
     -v \
     --collection transactions \
     --query '{"transaction_count": {"$gte": 50}}' 
     --out export.json \
     --jsonFormat canonical \
     "mongodb+srv://dbaTestAdmin@cluster1.xwgj1.mongodb.net/sample_analytics”


    mongoexport --uri="mongodb://mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/reporting?replicaSet=myReplicaSetName" --collection=events --out=events.json [additional options]

    mongoexport --host="myReplicaSetName/mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com" --collection=events --db=reporting --out=events.json [additional options]

    mongoexport --uri="mongodb://mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/reporting?replicaSet=myReplicaSetName&readPreference=secondary" --collection=events --out=events.json [additional options]
