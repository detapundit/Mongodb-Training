from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
import random
import time

client = MongoClient('mongodb://localhost:27017/')
db = client.loadtest

def generate_load(thread_id):
    """Generate continuous load"""
    while True:
        # Random operations
        operation = random.choice(['insert', 'query', 'aggregate', 'update'])
        
        if operation == 'insert':
            db.testCollection.insert_many([
                {
                    'thread': thread_id,
                    'data': 'x' * 5000,
                    'value': random.randint(1, 1000),
                    'timestamp': time.time()
                } for _ in range(100)
            ])
        
        elif operation == 'query':
            list(db.testCollection.find({'value': {'$gt': random.randint(1, 500)}}).limit(1000))
        
        elif operation == 'aggregate':
            list(db.testCollection.aggregate([
                {'$match': {'value': {'$gt': 400}}},
                {'$group': {'_id': '$thread', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]))
        
        elif operation == 'update':
            db.testCollection.update_many(
                {'value': {'$lt': 100}},
                {'$set': {'updated': time.time()}}
            )

# Run with multiple threads
with ThreadPoolExecutor(max_workers=8) as executor:
    for i in range(8):
        executor.submit(generate_load, i)
