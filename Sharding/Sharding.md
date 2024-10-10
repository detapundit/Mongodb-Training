Sharding is a method for distributing data across multiple machines. MongoDB uses sharding to support deployments with very large data sets and high throughput operations.

Database systems with large data sets or high throughput applications can challenge the capacity of a single server. 
For example, high query rates can exhaust the CPU capacity of the server. Working set sizes larger than the system's RAM stress the I/O capacity of disk drives.

A MongoDB sharded cluster consists of the following components:

shard: Each shard contains a subset of the sharded data. Each shard must be deployed as a replica set.

mongos: The mongos acts as a query router, providing an interface between client applications and the sharded cluster.

config servers: Config servers store metadata and configuration settings for the cluster. Config servers must be deployed as a replica set (CSRS).

![image](https://github.com/user-attachments/assets/0d2a0132-3689-4efc-a17a-2f20075c1ff3)

MongoDB shards data at the collection level, distributing the collection data across the shards in the cluster.

Shard Keys
MongoDB uses the shard key to distribute the collection's documents across shards. The shard key consists of a field or multiple fields in the documents.

Advantages of Sharding
Reads / Writes
MongoDB distributes the read and write workload across the shards in the sharded cluster, allowing each shard to process a subset of cluster operations. Both read and write workloads can be scaled horizontally across the cluster by adding more shards.

For queries that include the shard key or the prefix of a compound shard key, mongos can target the query at a specific shard or set of shards. These targeted operations are generally more efficient than broadcasting to every shard in the cluster.

Storage Capacity
Sharding distributes data across the shards in the cluster, allowing each shard to contain a subset of the total cluster data. 
As the data set grows, additional shards increase the storage capacity of the cluster.

High Availability
The deployment of config servers and shards as replica sets provide increased availability.

Even if one or more shard replica sets become completely unavailable, the sharded cluster can continue to perform partial reads and writes. 
That is, while data on the unavailable shard(s) cannot be accessed, reads or writes directed at the available shards can still succeed.

Sharded and Non-Sharded Collections
A database can have a mixture of sharded and unsharded collections. Sharded collections are partitioned and distributed across the shards in the cluster. Unsharded collections can be located on any shard but cannot span across shards.

![image](https://github.com/user-attachments/assets/fe29be65-566d-4248-9d8c-1d7c05b9f9a5)


Choose a Shard Key
The choice of shard key affects the creation and distribution of chunks across the available shards. The distribution of data affects the efficiency and performance of operations within the sharded cluster.

The ideal shard key allows MongoDB to distribute documents evenly throughout the cluster while also facilitating common query patterns.

Hashed Sharding
Hashed sharding uses either a single field hashed index or a compound hashed index as the shard key to partition data across your sharded cluster.

![image](https://github.com/user-attachments/assets/1c2f4538-c9cc-4ae3-ad34-925b85123021)


Ranged Sharding
Given a collection using a monotonically increasing value X as the shard key, using ranged sharding results in a distribution of incoming inserts similar to the following:

![image](https://github.com/user-attachments/assets/612072f6-c111-4a21-b63f-0551537339b4)


When you choose your shard key, consider:

    the cardinality of the shard key - uniqueness
    
    the frequency with which shard key values occur - same data appears
    
    whether a potential shard key grows monotonically - range ex. >70
    
    Sharding Query Patterns - scatter-gather queries
    
    Shard Key Limitations
    

Shard Key Selection
Ranged sharding is most efficient when the shard key displays the following traits:

        Large Shard Key Cardinality
        
        Low Shard Key Frequency
        
        Non-Monotonically Changing Shard Keys
