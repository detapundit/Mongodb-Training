**You can refer below link for more detailed info:**

    https://www.mongodb.com/docs/manual/administration/install-community/

Install MongoDB Community Edition: Linux

Platform Support
MongoDB 7.0 Community Edition supports the following 64-bit versions of Red Hat Enterprise Linux (RHEL), CentOS Linux, Oracle Linux [1], Rocky Linux, and AlmaLinux [2] on x86_64 architecture:

    RHEL / CentOS Stream / Oracle / Rocky / AlmaLinux 9

    RHEL / CentOS Stream / Oracle / Rocky / AlmaLinux 8

    RHEL / CentOS / Oracle 7

MongoDB only supports the 64-bit versions of these platforms.

MongoDB 7.0 Community Edition on RHEL / CentOS / Oracle / Rocky / AlmaLinux also supports the ARM64 architecture on select platforms.

#######################################################################################################################################

Follow these steps to install MongoDB Community Edition using the yum package manager.


1. Create a /etc/yum.repos.d/mongodb-org-7.0.repo file so that you can install MongoDB directly using yum:

       [mongodb-org-7.0]
       name=MongoDB Repository
       baseurl=https://repo.mongodb.org/yum/redhat/8/mongodb-org/7.0/x86_64/
       gpgcheck=1
       enabled=1
       gpgkey=https://pgp.mongodb.com/server-7.0.asc

2. Install the MongoDB packages

       sudo yum install -y mongodb-org

If only speific package, then:

       sudo yum install -y mongodb-org-7.0.14 mongodb-org-database-7.0.14 mongodb-org-server-7.0.14 mongodb-mongosh-7.0.14 mongodb-org-mongos-7.0.14 mongodb-org-tools-7.0.14

3. Start service

       sudo systemctl start mongod
       sudo service mongod start

4. You can verify that the mongod process has started successfully by checking the contents of the log file at /var/log/mongodb/mongod.log for a line reading

       [initandlisten] waiting for connections on port <port>

5. You can optionally ensure that MongoDB will start following a system reboot by issuing the following command:

       sudo chkconfig mongod on



