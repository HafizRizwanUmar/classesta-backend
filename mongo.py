import os
from pymongo import MongoClient

client = None
db = None

def get_mongo_db():
    global client, db
    if client is None:
        uri = os.getenv('MONGO_URI')
        if uri:
            client = MongoClient(uri)
            try:
                db = client.get_default_database()
            except:
                db = client['classesta']
    return db
