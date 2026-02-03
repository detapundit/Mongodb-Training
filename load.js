// Connect to your MongoDB instance
mongosh

// Create a test database and collection with sample data
use loadtest
for(let i = 0; i < 100000; i++) {
    db.testCollection.insertOne({
        index: i,
        data: "x".repeat(1000),
        timestamp: new Date(),
        nested: {
            field1: Math.random() * 1000,
            field2: "sample_" + i,
            array: Array(50).fill(0).map(() => Math.random())
        }
    });
}



// Run expensive aggregation pipelines
db.testCollection.aggregate([
    { $match: { index: { $gt: 0 } } },
    { $sort: { "nested.field1": -1 } },
    { $group: {
        _id: { $mod: ["$index", 100] },
        count: { $sum: 1 },
        avgField: { $avg: "$nested.field1" },
        data: { $push: "$$ROOT" }
    }},
    { $sort: { count: -1 } }
]);

// Run without indexes to stress CPU
db.testCollection.find({ "nested.field1": { $gt: 500 } }).sort({ index: -1 });

// Large document operations
db.testCollection.aggregate([
    { $lookup: {
        from: "testCollection",
        localField: "index",
        foreignField: "nested.field1",
        as: "joined"
    }},
    { $unwind: "$joined" }
]);

// Load large result sets into memory
db.testCollection.find({}).toArray();
