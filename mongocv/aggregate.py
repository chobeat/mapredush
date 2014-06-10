from matchdocument import MatchDocument
from groupdocument import GroupDocument
from querydocument import QueryDocument
from sortdocument import SortDocument
from pymongo import MongoClient

class Aggregate(list):

    def __init__(self, mongo_document):
        list.__init__(self)
        self.mongo_document = mongo_document

    def append(self, x):
        doc = x.getdoc()
        list.append(self, doc)

    def aggregate(self):
        self.results = self.mongo_document.aggregate(self)

    def printResults(self, fields=[]):
        results = self.results["result"]

        if fields==[]:
            for r in results:
                print r
        else:
            string = ""
            for r in results:
                for field in fields:
                    string += field+": "+str(r[field])+" "
                string += "\n"
            print string


"""
USE CASE
cars = MongoClient()["dbtest"]["cars"]

aggregate = Aggregate(cars)

oldestMaker = GroupDocument()
oldestMaker.setid("make")
oldestMaker.addmax("oldestYear","year")

aggregate += [oldestMaker.getdoc()]

sortOldestMaker = SortDocument()
sortOldestMaker.addfield("oldestYear")
aggregate += [sortOldestMaker.getdoc()]

aggregate.aggregate()

aggregate.printResults(["_id","oldestYear"])
"""