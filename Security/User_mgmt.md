1. Authentication
2. Authorization
3. Auditing


RBAC - Role based access control
Inbuilt roles - getRoles()

Enable Access Control

    sudo vi /etc/mongod.conf

Next, add the security.authorization setting under the security section of the configuration file:

    #security:
    security:
     authorization: enabled
    
    sudo systemctl restart mongod

Create the User Administrator

    db.createUser(
    {
    user: "mongoAdmin",
    pwd: passwordPrompt(),
    roles: [
    { role: "userAdminAnyDatabase", db: "admin" }
    ]
    }
    )


    quit()

Verify the User Administrator by login, localhost exception

    use admin
    db.getUsers()
