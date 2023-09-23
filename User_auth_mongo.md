## How to enable authorization/authentication in mongo

**The new section of the configuration file that enables authentication and authorization:**

    security:
      authorization: enabled

**Shutting down the server:**

    mongo admin --port 27001 --eval 'db.shutdownServer()'

**Restarting the server with mongod.conf:**

    mongod -f mongod.conf


**Connecting to MongoDB on port 27001:**

    mongo --port 27001

**Retrieving all users. After auth is enabled, it will allow to create one user with localhost, this is usually for admin user creation:**

    db.getUsers()
    
**Switching to the admin database:**

    use admin

**Creating the user administrator:**

    db.createUser({
      user: "globalAdminUser",
      pwd: "5xd49$4%0bef#6c&b*d",
      roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
    });

**Authenticating as the user administrator:**

    db.auth( "globalAdminUser", "5xd49$4%0bef#6c&b*d" )

**Creating a cluster administrator:**

    db.createUser({
      user: "clusterAdminAny",
      pwd: "a*0f7@2c6#b4f%$d6c^c7d",
      roles: [ "clusterAdmin" ]
    });
