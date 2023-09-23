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


  
