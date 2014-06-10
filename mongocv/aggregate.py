from matchdocument import MatchDocument
from groupdocument import GroupDocument
from sortdocument import SortDocument
from querydocument import QueryDocument

class Aggregate(list):

    def append(self, x):
        doc = x.getdoc()
        list.append(self, doc)

"""
q = QueryDocument("year")
q.addgt(2011)
match = MatchDocument(q)
group = GroupDocument("id")
group.addsum("count", 1)
group.addavg("media","age")
aggr = Aggregate()
aggr.append(match)
aggr.append(group)
sort = SortDocument()
sort.addfield("giannone")
aggr.append(sort)
print aggr
"""
