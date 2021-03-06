from pymongo import *
from pymongo.errors import *
from mongocv import *
from mongocv.aggregate import Aggregate
from mongocv.groupdocument import GroupDocument
from mongocv.matchdocument import MatchDocument
from mongocv.outdocument import OutDocument
from mongocv.querydocument import QueryDocument
from mongocv.document import Document

DB = MongoClient()["contestDB_E"]


def initDB():
    try:
        DB["texts"].ensure_index("textid")
        DB["texts"].ensure_index("timeline")
        DB["occurrences"].ensure_index("textid")
        DB["occurrences"].ensure_index("keyword")
        init_IDF()
    except CollectionInvalid:
        pass

def init_IDF():

    DB.create_collection("wordIDF")
    coll = DB["occurrences"]
    den = DB["texts"].count()
    group = GroupDocument("keyword")
    group.addpush("tweets", "textid")
    aggr = Aggregate()
    project = {"$project": {"keyword": 1, "idf": {"$divide": [den, {"$size": "$tweets"}]}}}
    out = OutDocument("wordIDF")

    aggr.append(group.getdoc())
    aggr.append(project)
    aggr.append(out.getdoc())

    coll.aggregate(aggr)


initDB()
