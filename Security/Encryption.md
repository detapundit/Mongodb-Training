Transport encryption (N/W) - secure data b/n client and DB - Ex TLS
Encryption at rest - Storage level - Safeguard data at rest - Key management, Insider threats, Attacks on data in memeory
In use encryption - Protects data when it leaves client , Client side Field level encryption(CSFLE). Client encrypt/decrypt, keys stored externally. Encrypt particular field

TLS - CA/Self signed

Encryp at rest: Encrypted storage engine (Enterprise only)

CSFLE - Community/Enterprise

TLS Steps:
Sample:

net:
  port: 27000
  bindIp: localhost,mongodb
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/tls/node1/mongodb.pem
    allowInvalidCertificates: true
    allowInvalidHostnames: true
    

Update the Configuration File for Each Server to Enable TLS

Set the net.tls.mode to requireTLS:

      net:
        tls:
          mode: requireTLS
          certificateKeyFile: /etc/tls/mongodb.pem

        replication:
          replSetName: TLSEnabledReplSet

Restart the MongoDB Service on Each Server

Initiate the Replica Set

    mongosh "mongodb://mongod0.replset.com/?tls=true&tlsCAFile=/etc/tls/root-ca.pem"
          rs.initiate(
        {
           _id: "TLSEnabledReplSet",
           version: 1
           members: [
              { _id: 0, host : "mongod0.replset.com" },
              { _id: 1, host : "mongod1.replset.com" },
              { _id: 2, host : "mongod2.replset.com" }
           ]
        }
      )

      mongosh "mongodb://mongod0.replset.com,mongod1.replset.com,mongod2.replset.com/?replicaSet=TLSEnabledReplSet&tls=true&tlsCAFile=/etc/tls/root-ca.pem"


Try to connect again, this time without TLS:

      mongosh "mongodb://mongod0.replset.com,mongod1.replset.com,mongod2.replset.com/?replicaSet=TLSEnabledReplSet" 
