##### LOG ######

To view logs from mongodb log

    sudo head -5 /var/log/mongodb/mongod.log

From DB console:
  
    show log <type>
    show logs
    db.adminCommand( { getLog:'global'} )


Log category:

FATAL
ERROR
WARNING
INFO
DEBUG


JQ tool to parse log files

    Install: yum install jq

Tutorial: https://jqlang.github.io/jq/tutorial/

Sample jq command. 

    jq '. | select(.msg | contains("transition"))' /var/log/mongodb/1/logs/mongod.log


Set a slowms Threshold in Mongo shell

To set a slowms threshold for an M10-or-above Atlas cluster or a self-managed MongoDB deployment, use the db.setProfilingLevel() method in mongosh. This method accepts two parameters: the profiler level and an options object. The profiler level is set to 0 to disable profiling completely, set to 1 for profiling operations that take longer than the threshold, and set to 2 for profiling all operations.

In the following example, the command leaves the profile disabled but changes the slowms threshold to 30 milliseconds:

    db.setProfilingLevel(0, { slowms: 30 })
    sudo grep "Slow query" /var/log/mongodb/mongod.log | jq

    vim /etc/mongod.conf

    systemLog:
      verbosity: 1
  
    systemLog:
    ...
    component:
    index:
      verbosity: 1

    sudo grep INDEX /var/log/mongodb/mongod.log | jq


**Log rotate**

    db.adminCommand( { logRotate : 1 } )


Automating Log Rotation with the logrotate Service

    sudo vim /etc/mongod.conf

    systemLog:
    destination: file
    logAppend: true
    path: /var/log/mongodb/mongod.log
    logRotate: reopen


    sudo vim /etc/logrotate.d/mongod.conf

    /var/log/mongodb/mongod.log {
     daily 
     size 
     rotate 10 
     missingok
     compress 
     compresscmd /usr/bin/bzip2 
     uncompresscmd /usr/bin/bunzip2 # command to uncompress the file
     compressoptions -9 # options for the compression utility
     compressext .bz2 # file format of the compressed archive
     delaycompress # wait to compress files until it's an opportune time
     notifempty # don't bother compressing if the log file is empty
     create 640 mongodb mongodb # creates the log  file with specific permissions
     sharedscripts # don't run multiple rotations at once
     postrotate # tell mongod to rotate, remove empty files
       /bin/kill -SIGUSR1 `cat /var/run/mongodb/mongod.pid 2>/dev/null` >/dev/null 2>&1
       find /var/log/mongodb -type f -size 0 -regextype posix-awk -regex "^\/var\/log\/mongodb\/mongod\.log\.[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}$" -execdir rm {} \; >/dev/null 2>&1
     endscript # end of the script
    }

    sudo systemctl restart mongod


## Testing
    sudo tail -F /var/log/mongodb/mongod.log
    sudo kill -SIGUSR1 $(pidof mongod)

