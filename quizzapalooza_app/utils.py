from pymongo import MongoClient

def connect_to_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['quizzapalooza_djongo']
    return db

