#You can access the admin database with the use command:

    use admin

#You can use grantRolesToUser() command to add the necessary roles to each of the user accounts.

#Grant the dbAdmin role on the emails database to emailsAdmin:
  
    db.grantRolesToUser(
       "emailsAdmin",
       [ { role: "dbAdmin", db: "emails" } ]
    )

#Grant the readWrite role on the emails database to emailsAdmin.

    db.grantRolesToUser(
       "emailsAdmin",
       [ { role: "readWrite", db: "emails" } ]
    )


#Grant the read role on the emailReports database to emailReportsUser.
 
  
    db.grantRolesToUser(
       "emailReportsUser",
       [ { role: "read", db: "emailReports" } ]
    )
