from document import Document
from pymongo import MongoClient
import sys
from anddocument import AndDocument
from ordocument import OrDocument
from nordocument import NorDocument

__author__ = 'civi'


class QueryDocument(Document):
    def __init__(self, field):
        Document.__init__(self)
        self.insidedoc = Document()
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

    def negate(self):
        self.insidedoc = {"$not": self.insidedoc.getdoc()}

    def addexists(self):
        self.addnormaloperator("$exists", True)

    def addnotexists(self):
        self.addnormaloperator("$exists", False)

    def addnormaloperator(self, operator, value):
        self.insidedoc.add(operator, value)

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

query = AndDocument([c1, c2])
print query
#print coll.find(query.getdoc()).count()
"""

"""
c = QueryDocument("year")
c.addgt(2011)
c.negate()
print c
"""

