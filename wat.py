
from pymongo import MongoClient


client = MongoClient()

db = client.ufcstats.taleofthetape.find()

print(db)