from django.shortcuts import render

from django.http import HttpResponse

data = ""

def index(request):
    return HttpResponse(f"Hello, world. You're at the polls index. {data}")

import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["academic"]

dblist = myclient.list_database_names()
if "academic" in dblist:
  print("The database exists.")
  collist = mydb.list_collection_names()
  if "academics" in collist:
      print("The collection exists.")
      mydict = { "_id": 1, "name": "John", "address": "Highway 37" }
      mycol = mydb["academics"]
      #x = mycol.insert_one(mydict)
      for x in mycol.find():
        data = x

else:
    print("The database is not exists.")