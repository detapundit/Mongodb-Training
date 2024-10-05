

    rs.initiate( {
       _id : "myTest",
       members: [
          { _id: 0, host: "10.128.0.14:27017" },
          { _id: 1, host: "10.128.0.15:27017" },
          { _id: 2, host: "10.128.0.16:27017" }
       ]
    })


To add

    rs.add( { host: "mongodb3.example.net:27017" } )

rs.addArb("m1.example.net:27017")



Remove a Member Using rs.remove()
Shut down the mongod instance for the member you wish to remove. To shut down the instance, connect using mongosh and use the db.shutdownServer() method.

Connect to the replica set's current primary. To determine the current primary, use db.hello() while connected to any member of the replica set.

Use rs.remove() in either of the following forms to remove the member:

    rs.remove("mongod3.example.net:27017")
    rs.remove("mongod3.example.net")

Remove a Member Using rs.reconfig()

Procedure
Shut down the mongod instance for the member you wish to remove. To shut down the instance, connect using mongosh and use the db.shutdownServer() method.

Connect to the replica set's current primary. To determine the current primary, use db.hello() while connected to any member of the replica set.

Issue the rs.conf() method to view the current configuration document and determine the position in the members array of the member to remove:


To make hidden node

    cfg = rs.conf()
    cfg.members[0].priority = 0
    cfg.members[0].hidden = true
    rs.reconfig(cfg)


Adjust member priority

    cfg = rs.conf()
    
    cfg.members[0].priority = 0.5
    cfg.members[1].priority = 2
    cfg.members[2].priority = 2
    
    rs.reconfig(cfg)


