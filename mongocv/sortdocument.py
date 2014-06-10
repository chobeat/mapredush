from document import Document

__author__ = 'civi'

class SortDocument(Document):
    def __init__(self):
        Document.__init__(self)
        self.insidedoc = Document()

    def addfield(self, field):
        self.insidedoc.add(field, 1)

    def addfieldreverse(self, field):
        self.insidedoc.add(field, -1)

    def __str__(self):
        self.add("$sort", self.insidedoc)
        return str(self.getdoc())

    def getdoc(self):
        self.add("$sort", self.insidedoc)
        return self.doc