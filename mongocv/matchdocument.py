from document import Document
from querydocument import QueryDocument
from groupdocument import GroupDocument

__author__ = 'civi'

class MatchDocument(Document):
    def __init__(self):
        Document.__init__(self)

    def addquerydoc(self, qdoc):
        self.add("$match",qdoc.getdoc())


"""
USE CASE:
q = QueryDocument()
q.setfield("score")
q.addgt(70)
q.addlte(90)
match = MatchDocument()
match.addquerydoc(q)

#aggregate time!
group = GroupDocument()
group.setid("id")
group.addsum("count", 1)

#aggregation pipeline example
print [match.getdoc(),group.getdoc()]

"""