from document import Document
from pymongo import MongoClient
import sys

__author__ = 'civi'


class QueryDocument(Document):
    def __init__(self, field=""):
        Document.__init__(self)
        self.insidedoc = Document()
        if field!="":
            self.field = field

    def addeq(self,value):
        self.add(self.field, value)

    def addgt(self, value):
        self.addnormaloperator("$gt", value)

    def addgte(self, value):
        self.addnormaloperator("$gte", value)

    def addlt(self, value):
        self.addnormaloperator("$lt", value)

    def addlte(self, value):
        self.addnormaloperator("$lte", value)

    def addne(self, value):
        self.addnormaloperator("$ne", value)

    def addin(self,value):
        self.addnormaloperator("$in", value)

    def addnin(self,value):
        self.addnormaloperator("$nin", value)

    def addor(self, value):
        self.addlistoperator("$or", value)

    def addand(self, value):
        self.addlistoperator("$and", value)

    def addnor(self, value):
        self.addlistoperator("$nor", value)

    def negate(self):
        self.insidedoc = {"$not": self.insidedoc.getdoc()}

    def addexists(self):
        self.addnormaloperator("$exists", True)

    def addnotexists(self):
        self.addnormaloperator("$exists", False)

    def addlistoperator(self,operator, value):
        self.addnormaloperator(operator, self.docfromlist(value))

    def addnormaloperator(self, operator, value):
        self.insidedoc.add(operator, value)

    def docfromlist(self, qdocs):
        lst = list()
        for qdoc in qdocs:
            lst.append(qdoc.getdoc())
        return lst

    def getdoc(self):
        try:
            if self.insidedoc:
                self.add(self.field, self.insidedoc)
            return self.doc
        except AttributeError:
            return self.insidedoc.getdoc()

    def __str__(self):
        return str(self.getdoc())

"""
coll = MongoClient()["ginfo-exercise"]["cars"]

c1 = QueryDocument("year")
c1.addgt(2011)
c2 = QueryDocument("top_speed")
c2.addlte(300)
c2.addne(0)

query = QueryDocument()
query.addand([c1, c2])
print coll.find(query.getdoc()).count()

"""

"""
c = QueryDocument("year")
c.addgt(2011)
c.negate()
print c
"""

