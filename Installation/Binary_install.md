Links:

Mongo server download link:
https://www.mongodb.com/try/download/community

Mongo Shell download link:
https://www.mongodb.com/docs/mongodb-shell/install/

**DEPENDENCIES**

    yum install openssl
    yum install libcurl
    yum install xz-libs

**DOWNLOAD MONGODB VERSION AS PER OS FLAVOR, untar and unzip and copy to /usr/local/bin**

    wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel90-7.0.14.tgz
    tar -xzvf mongodb-linux-x86_64-rhel90-7.0.14.tgz 
    cp /home/demouser/mongodb-linux-x86_64-rhel90-7.0.14/bin/* /usr/local/bin/
    chmod +x /usr/local/bin/*

DOWNLOAD MONGO SHELL, untar and unip and copy to usr/local/bin

    wget https://downloads.mongodb.com/compass/mongosh-1.10.6-linux-x64.tgz
    tar -zxvf mongosh-1.10.6-linux-x64.tgz 
    cp /home/demouser/mongosh-1.10.6-linux-x64/bin/* /usr/local/bin/

**CREATE DATA DIR AND LOG FILE DIR**

    mkdir -p /var/lib/mongo
    mkdir -p /var/log/mongodb

**CREATE A USER AND PROVIDE PERMISSIONS**

    useradd mongod
    chown -R mongod:mongod /var/lib/mongo
    chown -R mongod:mongod /var/log/mongodb

**CHANGE SESTATUS TO PERMISSIVE**

    sestatus
    setenforce 0

**START MONGO DAEMON WITHOUT CONF FILE USING PARAMETERS IN CMD LINE. IF YOU WANT TO RUN THIS PROCESS AS MONGOD USER THEN SWITCH TO MONGOD BY su - mongod**

    /usr/local/bin/mongod --dbpath /var/lib/mongo --logpath /var/log/mongodb/mongod.log --fork

**START MONGO DAEMON WITH CONF FILE. CREATE A CONF FILE INN /etc/mongod.conf with required parameters**

    /usr/local/bin/mongod --conf /etc/mongod.conf --fork

**CONNECTING TO MONGODB INSTANCE**

    /usr/local/bin/.mongosh
