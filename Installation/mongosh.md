            config
            
            config.get('enableTelemetry') // returns true or false
            
            config.set('enableTelemetry', false)
            
            config.reset('enableTelemetry')

Windows: `mongosh.cfg`, in the same directory as the `mongosh.exe` binary.

macOS:
/usr/local/etc/mongosh.conf
/etc/mongosh.conf
/opt/homebrew/etc/mongosh.conf

Linux: /etc/mongosh.conf

The mongosh.conf file uses YAML format. The following code shows how to configure the displayBatchSize, inspectDepth, and redactHistory options in mongosh.conf:

      mongosh: 
       displayBatchSize: 50 
       inspectDepth: 20 
       redactHistory: "remove-redact"

  Configure mongosh by Using the --eval Flag

      mongosh --eval "disableTelemetry()"
  
You can also use the --eval flag to run queries and other commands. For example, to run a query for some documents, you would run the following command:

      mongosh --eval "db.accounts.find().limit(3)" --quiet
