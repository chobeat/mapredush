from collections import Counter
from pymongo.mongo_client import MongoClient
from mongocv.aggregate import Aggregate
from mongocv.groupdocument import GroupDocument
from mongocv.matchdocument import MatchDocument
from mongocv.outdocument import OutDocument
from mongocv.querydocument import QueryDocument
from mongocv.document import Document
from inizializzatore import *
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

memotfidf={}
def tfidf(tweetid):

    try:
	return memotfidf[tweetid]
    except KeyError:
        res = dict()
        coll = DB["wordIDF"]
        tf = tweetid2freqdict(tweetid)
        for word in tf:
           query = Document()
           query.add("_id", word)
           idf = math.log(coll.find_one(query.getdoc())["idf"])
           res[word] = tf[word]*idf
       	memotfidf[tweetid]=res
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
import csv
from itertools import combinations
def timelineSimilarityMatrix(threshold,path):
    group=GroupDocument("timeline")
    aggr=Aggregate()
    aggr.append(group.getdoc())

    timelines=DB['texts'].aggregate(aggr)['result']

    timelines = [c['_id'] for c in timelines]

    couples = combinations(timelines, 2)
    with open(path,'wb') as csvfile:
	row=csv.writer(csvfile,dialect="excel-tab")
        [row.writerow([c[0], c[1], timelineSimilarity(c[0],c[1],threshold)]) for c in couples]



def timelineSimilarity(timeline1, timeline2, threshold):
    listatweet1 = timeline2tweets(timeline1)
    listatweet2 = timeline2tweets(timeline2)

    if len(listatweet1) <= len(listatweet2):
        result = computeDice(listatweet1, listatweet2, threshold)
    else:
        result = computeDice(listatweet2, listatweet1, threshold)

    return result


def computeDice(listatweet1, listatweet2, threshold):
    counter = 0
    for tweet1 in listatweet1:
        for tweet2 in listatweet2:
	    c=cosineSimilarity(tweet1, tweet2)

            if c >= float(threshold):

                counter += 1

    return (float(2 * counter))/(len(listatweet1) + len(listatweet2))

def mainConsegna(args):
    initDB()
    functions=[tfidf, cosineSimilarity, timelineSimilarityMatrix]

    if len(args)<2:
        print "Dammi un ID operazione"
        return

    func=int(args[1])-1
    if func>2 or func<0:
        print "ID Operazione non valido"
        return
    else:
        print functions[func](*args[2:])

