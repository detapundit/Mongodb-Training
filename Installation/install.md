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


