from document import Document

__author__ = 'civi'

class CompositeQueryDocument(Document):
    def __init__(self, operator, list):
        Document.__init__(self)
        lst = [qdoc.getdoc() for qdoc in list]
        self.add(operator,lst)