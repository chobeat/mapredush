from collections import Counter
from pymongo.mongo_client import MongoClient
from mongocv.aggregate import Aggregate
from mongocv.groupdocument import GroupDocument
from mongocv.matchdocument import MatchDocument
from mongocv.outdocument import OutDocument
from mongocv.querydocument import QueryDocument
from mongocv.document import Document
import math
import sys
__author__ = 'civi'

DB = MongoClient()["contestDB_E"]

def tweetid2words(tweetid):
    coll = DB["occurrences"]
    query = Document()
    query.add("textid",tweetid)
    match = MatchDocument(query)

    group = GroupDocument("textid")
    group.addpush("words", "keyword")

    aggr = Aggregate()
    aggr.append(match.getdoc())
    aggr.append(group.getdoc())

    res = coll.aggregate(aggr)

    result = res["result"]

    if len(result)==0:
	print "Tweet ID non valido"
	return []
    words=result[0]["words"]
    return words

def getfreqdict(words):
    den = len(words)
    wordsVector = Counter(words)
    freqdict = {word: wordsVector[word]/float(den) for word in wordsVector}
    return freqdict

def tweetid2freqdict(tweetid):
    words = tweetid2words(tweetid)
    return getfreqdict(words)

def tfidf(tweetid):
    res = dict()
    coll = DB["wordIDF"]
    tf = tweetid2freqdict(tweetid)
    for word in tf:
        query = Document()
        query.add("_id", word)
        idf = math.log(coll.find_one(query.getdoc())["idf"])
        res[word] = tf[word]*idf
    return res

def mainConsegna(args):

	functions=[tfidf,"a","b"]
	func=int(args[1])-1
	if func>2 or func<0:
		print "ID Operazione non valido"
	else:
		print functions[func](*args[2:])


