from mongocv.groupdocument import GroupDocument
from mongocv.limitdocument import LimitDocument
from mongocv.outdocument import OutDocument
from mongocv.sortdocument import SortDocument

__author__ = 'Francesco'

'''ultimo esercizio dell'ultima esercitazione di lab'''
import pymongo
from mongocv.querydocument import QueryDocument
from pymongo import MongoClient
from mongocv.aggregate import Aggregate
from mongocv.document import Document
import json

coll = MongoClient()['carsDB']['carsColl']
agg = Aggregate()
doc = Document()

'''il primo  il nome del campo che viene visualizzato. Il secondo  il nome del campo che si prende
dalla collezione entrante'''

doc.add('year', 'year')
doc.add('make', 'make')
group1 = GroupDocument(doc)
group1.addsum('numberOfProducedModels', 1)

doc2 = Document()
doc2.add('year', '_id.year')
doc2.add('numberOfProducedModels', 'numberOfProducedModels')
group2 = GroupDocument(doc2)
group2.addpush('makers', '_id.make')

sort = SortDocument()
limit = LimitDocument(10)
sort.addfield('_id.numberOfProducedModels')

out = OutDocument('outcollpycharmsortedlimit')

agg.append(group1)
agg.append(group2)
agg.append(limit)
agg.append(sort)
agg.append(out)


print agg

print json.dumps(coll.aggregate(agg), indent=4)
