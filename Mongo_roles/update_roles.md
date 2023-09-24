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

#You can use createRole() command to create the new role and privileges.

#Solved Code
#Create the role insertAndFindTransactions with privileges on the transactions database, specifically on all collections where it has #the specific actions of insert and of find:

      db.createRole(
        {
          role: "insertAndFindTransactions",
          privileges: [
            { resource: { db: "transactions", collection: "" }, actions: [ "insert", "find" ] },
          ],
          roles: [ ]
        }
      )

#You can use updateUser() command to create the new role and privileges.

#Solved Code

#Change the password for readWriteInventoryUser to be 6c%dbe&7dc!ee1#d in the admin database:

         db.updateUser(
               "readWriteInventoryUser",
               {
                 pwd: "6c%dbe&7dc!ee1#d"
               }
            )
