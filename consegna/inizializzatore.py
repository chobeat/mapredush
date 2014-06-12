from pymongo import *

def connToDB(collection):
	client=MongoClient()
	db=client.contestDB_E
	return db[collection]

