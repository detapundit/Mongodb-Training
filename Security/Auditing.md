**Locate the Audit Log File**

    cat /etc/mongod.conf
    auditLog:
      destination: file
      format: JSON
      path: /var/log/mongodb/auditLog.json
    
      sudo tail /var/log/mongodb/auditLog.json | jq
