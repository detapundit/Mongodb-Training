**Locate the Audit Log File**
Audit file can be print in file, syslog, console(Linux,Macos)

    cat /etc/mongod.conf
    auditLog:
      destination: file
      format: JSON
      path: /var/log/mongodb/auditLog.json
    
      sudo tail /var/log/mongodb/auditLog.json | jq

Incorrect login : mongosh localhost:27017/admin --username badUser --password incorrectPassword
Check audit file
