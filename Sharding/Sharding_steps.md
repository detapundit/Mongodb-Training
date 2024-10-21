We will setup first config server, then 2 shard servers and 1 Mongos

**CONFIG SERVER - 3 member replicaset configuration**

1. Install Mongodb
2. Stop mongodb service
3. Edit Mongo conf file to update/add below parameters
4. For config servers, mention clusterRole as configsvr in all 3 nodes of config replicaset.
5. replSetName - Should be same across all 3 nodes of config servers
6. bindIp - Mention IP address of individual host
7. port - Change port to 27019

        port: 27019   => Update port to 27019
        
        sharding:
          clusterRole: configsvr
        
        replication:
          replSetName: "csrepset"
        
        net:
          bindIp: 10.128.0.18

8. Restart all 3 nodes of config server
9. Connect to any 1 node of config server

        mongosh --port 27019 --host 10.128.0.18
   
10. Initiate the replicaset

        rs.initiate(
        {
          _id: "csrepset",
          configsvr: true,
          members: [
            { _id : 0, host : "10.128.0.18:27019" },
            { _id : 1, host : "10.128.0.19:27019" },
            { _id : 2, host : "10.128.0.20:27019" }
          ]
        }
        )

11. Check replicaset status if all 3 members have joined and are in healthy state


**SHARD 1 - 3 member replicaset setup - Step 1 to 8 is to be performed on all 3 nodes of shard1**

1. Install Mongodb
2. Stop mongodb service
3. Edit Mongo conf file to update/add below parameters
4. For shard servers, mention clusterRole as shardsvr in all 3 nodes of shard 1 replicaset.
5. replSetName - Should be same across all 3 nodes of shard 1 servers
6. bindIp - Mention IP address of individual host
7. port - Change port to 27018

         port: 27018 => Update port to 27018

        sharding:
            clusterRole: shardsvr
        replication:
            replSetName: "shard1"
        net:
            bindIp: 10.128.0.21

8. Restart all 3 nodes of shard1
9. Connect to any 1 node of shard1

        mongosh --port 27018 --host 10.128.0.21
   
10. Initiate the replicaset

        rs.initiate(
        {
          _id : "shard1",
          members: [
            { _id : 0, host : "10.128.0.21:27018" },
            { _id : 1, host : "10.128.0.22:27018" },
            { _id : 2, host : "10.128.0.23:27018" }
          ]
        }
        )

11. Check replicaset status if all 3 members have joined and are in healthy state


**SHARD 2 - 3 member replicaset setup - Step 1 to 8 is to be performed on all 3 nodes of shard2**

1. Install Mongodb
2. Stop mongodb service
3. Edit Mongo conf file to update/add below parameters
4. For shard servers, mention clusterRole as shardsvr in all 3 nodes of shard2 replicaset.
5. replSetName - Should be same across all 3 nodes of shard2 servers
6. bindIp - Mention IP address of individual host
7. port - Change port to 27018

         port: 27018 => Update port to 27018

        sharding:
            clusterRole: shardsvr
        replication:
            replSetName: "shard2"
        net:
            bindIp: 10.128.0.24

8. Restart all 3 nodes of shard2
9. Connect to any 1 node of shard2

        mongosh --port 27018 --host 10.128.0.24
   
10. Initiate the replicaset

        rs.initiate(
        {
          _id : "shard2",
          members: [
            { _id : 0, host : "10.128.0.24:27018" },
            { _id : 1, host : "10.128.0.25:27018" },
            { _id : 2, host : "10.128.0.26:27018" }
          ]
        }
        )

11. Check replicaset status if all 3 members have joined and are in healthy state


**Mongos setup - Single node**

1. Install Mongodb
2. Stop mongodb service
3. Start mongos service via command line by providing config server details. We need to config server replicaset name and IP address:port of all 3 nodes of config server

        mongos --configdb csrepset/10.128.0.18:27019,10.128.0.19:27019,10.128.0.20:27019 --bind_ip 10.128.0.17 &

4. Connect to mongos

       mongos --host 10.128.0.17

5. Add the shard details using addShard command. Please find sample command below.
   sh.addShard( "<replSetName>/s1-mongo1.example.net:27018,s1-mongo2.example.net:27018,s1-mongo3.example.net:27018")

6. As we have 2 shards( Shard1 & Shard 2), we will add it in mongos

sh.addShard( "shard1/10.128.0.21:27018,10.128.0.22:27018,10.128.0.23:27018")
sh.addShard( "shard2/10.128.0.24:27018,10.128.0.25:27018,10.128.0.26:27018")

7. We can check shard status by running below command

        sh.status()

8. Now we enable sharding for sample collection called cities under populations database. Create a database called populations

sh.enableSharding("populations")
sh.shardCollection("populations.Cities", { "country": "hashedhashed" })

9. Now we will insert 20 documents under cities collection

        use populations
        db.Cities.insertMany([
            {"name": "Seoul", "country": "South Korea", "continent": "Asia", "population": 25.674 },
            {"name": "Mumbai", "country": "India", "continent": "Asia", "population": 19.980 },
            {"name": "Lagos", "country": "Nigeria", "continent": "Africa", "population": 13.463 },
            {"name": "Beijing", "country": "China", "continent": "Asia", "population": 19.618 },
            {"name": "Shanghai", "country": "China", "continent": "Asia", "population": 25.582 },
            {"name": "Osaka", "country": "Japan", "continent": "Asia", "population": 19.281 },
            {"name": "Cairo", "country": "Egypt", "continent": "Africa", "population": 20.076 },
            {"name": "Tokyo", "country": "Japan", "continent": "Asia", "population": 37.400 },
            {"name": "Karachi", "country": "Pakistan", "continent": "Asia", "population": 15.400 },
            {"name": "Dhaka", "country": "Bangladesh", "continent": "Asia", "population": 19.578 },
            {"name": "Rio de Janeiro", "country": "Brazil", "continent": "South America", "population": 13.293 },
            {"name": "São Paulo", "country": "Brazil", "continent": "South America", "population": 21.650 },
            {"name": "Mexico City", "country": "Mexico", "continent": "North America", "population": 21.581 },
            {"name": "Delhi", "country": "India", "continent": "Asia", "population": 28.514 },
            {"name": "Buenos Aires", "country": "Argentina", "continent": "South America", "population": 14.967 },
            {"name": "Kolkata", "country": "India", "continent": "Asia", "population": 14.681 },
            {"name": "New York", "country": "United States", "continent": "North America", "population": 18.819 },
            {"name": "Manila", "country": "Philippines", "continent": "Asia", "population": 13.482 },
            {"name": "Chongqing", "country": "China", "continent": "Asia", "population": 14.838 },
            {"name": "Istanbul", "country": "Turkey", "continent": "Europe", "population": 14.751 }
        ])

10. You can check distribution of data by using below command

          db.Cities.getShardDistribution()


   

