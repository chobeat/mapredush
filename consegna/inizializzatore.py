from pymongo import *
from pymongo.errors import *
from mongocv import *

def connToDB(collection):
	client=MongoClient()
	db=client.contestDB_E
	return db[collection]

def initDB():
	try:
		db=connToDB("occurrences").database
		print "Inizializzazione database"
		init_IDF(db.wordIDF)
	except CollectionInvalid:
		pass

def init_IDF(coll):
	db=connToDB("occurrences").database
	db.wordIDF.drop()
	db.create_collection("wordIDF")
	occurrences=connToDB("occurrences")
	num=occurrences.count()
	print num
	res=occurrences.aggregate()

initDB()
