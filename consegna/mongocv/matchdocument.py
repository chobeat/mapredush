from document import Document
from querydocument import QueryDocument
from groupdocument import GroupDocument

__author__ = 'civi'

class MatchDocument(Document):
    def __init__(self, qdoc):
        Document.__init__(self)
        self.add("$match", qdoc.getdoc())


"""

q = QueryDocument("score")
q.addgt(70)
q.addlte(90)
match = MatchDocument(q)
group = GroupDocument("id")
group.addsum("count", 1)

#aggregation pipeline example
print [match.getdoc(),group.getdoc()]
"""
