**RBAC**

**Assign a Built-In Role to a Database User**

    use admin
    db.createUser(
      {
        user: "analystUser",
        pwd: passwordPrompt(),        
        roles: [
          { role: "read", db: "sample_analytics" },
        ]
      }

      mongosh "mongodb://analystUser@localhost:27017/sample_analytics?authSource=admin"

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
