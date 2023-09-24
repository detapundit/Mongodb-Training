#  All-Database Roles

**The following roles are available on the admin database and provide privileges which apply to all databases except local and config:**

    readAnyDatabase
    Explanation: Provides the same read-only privileges as read on all databases except local and config. The role also provides the       listDatabases action on the cluster as a whole.

**See also the clusterManager and clusterMonitor roles for access to the config and local databases.**


    readWriteAnyDatabase
    Explanation: Provides the same privileges as readWrite on all databases except local and config. The role also provides: the           listDatabases action on the cluster as a whole the compactStructuredEncryptionData action

    userAdminAnyDatabase
    Explanation: Provides the same access to user administration operations as userAdmin on all databases except local and config.

    userAdminAnyDatabase
     also provides the following privilege actions on the cluster: authSchemaUpgrade, invalidateUserCache, listDatabases
    Explanation: The role provides the following privilege actions on the system.users and system.roles collections on the admin           database, and on legacy system.users collections from versions of MongoDB prior to 2.6:

    userAdminAnyDatabase
    role does not restrict the privileges that a user can grant. As a result, userAdminAnyDatabase users can grant themselves               privileges in excess of their current privileges and even can grant themselves all privileges, even though the role does not            explicitly authorize privileges beyond user administration. This role is effectively a MongoDB system superuser.

    dbAdminAnyDatabase
    Provides the same privileges as dbAdminon all databases except local and config. The role also provides the listDatabases action on     the cluster as a whole.

**Starting in MongoDB 5.0, **

    dbAdminAnyDatabase
    includes the applyOps privilege action.

**Superuser Roles**
*Several roles provide either indirect or direct system-wide superuser access.

**The following roles provide the ability to assign any user any privilege on any database, which means that users with one of these roles can assign themselves any privilege on any database:**

    dbOwner
     role, when scoped to the admin database
    
    userAdmin
     role, when scoped to the admin database
    
    userAdminAnyDatabase
     role

**The following role provides full privileges on all resources:**

    root
    Provides access to the operations and all the resources of the following roles combined:
    
    readWriteAnyDatabase
    
    dbAdminAnyDatabase
    
    userAdminAnyDatabase
    
    clusterAdmin
    
    restore
    
    backup

    Also provides the validate privilege action on system. collections.

**Changed in version 6.0: The root role includes find and remove privileges on the system.preimages collection in the config database.**
