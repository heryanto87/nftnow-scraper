from pymongo import MongoClient

def connect():
  uri = "mongodb://localhost:27017"
  client = MongoClient(uri)
  db = client["nftnow"]
  return db