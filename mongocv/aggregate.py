from matchdocument import MatchDocument
from groupdocument import GroupDocument
from sortdocument import SortDocument
from querydocument import QueryDocument

class Aggregate(list):

    def append(self, x):
        doc = x.getdoc()
        list.append(self, doc)


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
sort = SortDocument()
sort.addfield("giannone")
aggr.append(sort)
print aggr


"""


