import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['publications']

searcheds = db['searcheds']

record = {"yayin adi":"emre"}
searcheds.insert_one(record)


searchin = searcheds.find()

