from pymongo import MongoClient
from pprint import pprint

def init():
    client = MongoClient("localhost")
    db = client.parsed
    return db

def insert_tree(connection, tree):
    db.parsed.insert_one(tree)

def get_all(connection):
    for el in db.parsed.find():
        yield el

def print_all(connection):
    for el in db.parsed.find():
        pprint(el)