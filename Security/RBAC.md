**RBAC - Role based access control**

List of built-in roles - https://www.mongodb.com/docs/v5.2/reference/built-in-roles/

MongoDB stores all role information in the admin.system.roles collection in the admin database.


To create a role in a database, you must have:

the createRole action on that database resource.

the grantRole action on that database to specify privileges for the new role as well as to specify roles to inherit from.

**User defined role (Sample)**

        use admin
        db.createRole(
           {
             role: "manageOpRole", 
             privileges: [
               { resource: { cluster: true }, actions: [ "killop", "inprog" ] },
               { resource: { db: "", collection: "" }, actions: [ "killCursors" ] }
             ],
             roles: []
           }
        )


**Assign a Built-In Role to a Database User**

    use admin
    db.createUser(
      {
        user: "financeUser",
        pwd: passwordPrompt(),        
        roles: [
          { role: "read", db: "sample_supplies" },
          { role: "readWrite", db: "sample_analytics" },
        ]
      }

      mongosh "mongodb://financeUser@localhost:27017/sample_analytics?authSource=admin"

      db.accounts.findOne()

**Remove a Built-In Role from a Database User**

      use admin
      db.getUser("financeUser")
    
        db.revokeRolesFromUser(
        "financeUser",
        [
          { role: "read", db: "sample_training" }
        ]
    )

        db.getUser("financeUser")


**Modify password for a user**

Syntax: db.changeUserPassword("username", "new_password")

        db.changeUserPassword("reporting", "SOh3TbYhxuLiW8ypJPxmt1oOfL")
