from document import Document

__author__ = 'civi'


class QueryDocument(Document):
    def __init__(self):
        Document.__init__(self)

    def addnormalcondition(self, key, operator, condition):
        tmp = Document()
        tmp.add(operator, condition)
        self.add(key, tmp)

    def addcomplexcondition(self, key, opcondlist):
        """
        :param key: The key value
        :param opcondlist: A list of tuples or documents (operator,condition)
        :return: complexcondition added to the document
        """
        tmp = Document()
        for k, v in opcondlist:
            tmp.add(k, v)
        self.add(key, tmp)


    def addlistcondition(self, operator, lst):
        """
        :param operator: The operator ($and, $or, ...)
        :param lst: A list of QueryDocument
        :return: the listcondition is added to the document
        """
        tmp = []
        for qdoc in lst:
            tmp.append(qdoc.getdoc())
        self.add(operator, tmp)

"""
USE CASE 1: normalcondition and complex condition

a = QueryDocument()
a.addnormalcondition("year", "$gt", 2011)
tmp = [("$ne", 0), ("$lte", 300)]
a.addcomplexcondition("top_speed", tmp)
b = QueryDocument()
conditions = list()
"""

"""
USE CASE 2: listcondition
c1 = QueryDocument()
c1.addnormalcondition("year","$gt",2011)
c2 = QueryDocument()
c2.addnormalcondition("top_speed","$lte",300)
conditions = [c1,c2]
b = QueryDocument()
b.addlistcondition("$and", conditions)
print b

"""
