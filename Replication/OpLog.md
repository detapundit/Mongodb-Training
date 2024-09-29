**OPLOG**

Oplog is a capped collection. Oldest entries is rewritten

![image](https://github.com/user-attachments/assets/c3695d41-e690-406b-95fc-d39e07a87cbe)

Oplog size is 5% of available disk space or max 50GB

    use sample_supplies
    
    db.sales.updateMany({}, {$inc: {"customer.satisfaction": 1}});
    
    use local
    
    show collections
    
    db.oplog.rs.find({"ns" : "sample_supplies.sales"}).sort({$natural: -1}).limit(5)
    
    rs.printReplicationInfo()
    
    rs.printSecondaryReplicationInfo()
