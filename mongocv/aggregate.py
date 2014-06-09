from matchdocument import MatchDocument
from groupdocument import GroupDocument
from querydocument import QueryDocument

class Aggregate(list):

    def append(self, x):
        doc = x.getdoc()
        list.append(self, doc)

    def getaggregate(self):
        return self.pipeline


"""
USE CASE

q = QueryDocument()
q.setfield("year")
q.addgt(2011)
match = MatchDocument()
match.addquerydoc(q)
group = GroupDocument()
group.setid("id")
group.addsum("count",1)
aggr = Aggregate()
aggr.append(match)
aggr.append(group)
print aggr
"""




