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

def timeline2tweets(timeline):
    coll = DB["texts"]
    aggr = Aggregate()
    query = Document()
    query.add("timeline",timeline)
    match = MatchDocument(query)
    group = GroupDocument("timeline")
    group.addpush("tweets", "textid")
    aggr.append(match)
    aggr.append(group.getdoc())
    return coll.aggregate(aggr)["result"][0]["tweets"]


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

    words = result[0]["words"]
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


def cosineSimilarity(tweetID1, tweetID2):
    words1 = tfidf(tweetID1)
    words2 = tfidf(tweetID2)

    keys1 = words1.keys()
    keys2 = words2.keys()

    commonWords = set(keys1) & set(keys2)

    num = sum([words1[value] * words2[value] for value in commonWords])

    #somme al quadrato
    sumDoc1 = sum([math.pow(words1[value], 2) for value in keys1])
    sumDoc2 = sum([math.pow(words2[value], 2) for value in keys2])
    den = math.sqrt(sumDoc1) * math.sqrt(sumDoc2)
    result = 0

    try:
        return float(num) / den
    except Exception:
        return 0.0

#print cosineSimilarity("276731870660673536","277893035206012928")

timeline2tweets("Pierferdinando")

"""
if __name__=="__main__":
    functions = [tfidf, cosineSimilarity, "b"]
    func = int(sys.argv[1])-1
    if func>2 or func<0:
        print "ID Operazione non valido"
    else:
        print functions[func](*sys.argv[2:])
"""
