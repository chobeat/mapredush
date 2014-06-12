from collections import Counter
from pymongo.mongo_client import MongoClient
from mongocv.aggregate import Aggregate
from mongocv.groupdocument import GroupDocument
from mongocv.matchdocument import MatchDocument
from mongocv.outdocument import OutDocument
from mongocv.querydocument import QueryDocument
from mongocv.document import Document
import math

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
    aggr.append(match)
    aggr.append(group)

    res = coll.aggregate(aggr)
    words = res["result"][0]["words"]
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

def initIDFCollection():
    coll = DB["occurrences"]
    den = DB["texts"].count()
    group = GroupDocument("keyword")
    group.addpush("tweets", "textid")
    aggr = Aggregate()
    project = {"$project": {"keyword": 1, "idf": {"$divide": [den, {"$size": "$tweets"}]}}}
    out = OutDocument("wordIDF")

    aggr.append(group)
    aggr.append(project)
    aggr.append(out)

    coll.aggregate(aggr)["result"]
