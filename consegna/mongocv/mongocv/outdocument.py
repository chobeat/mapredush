from document import Document

__author__ = 'civi'


class OutDocument(Document):
    def __init__(self, documentname):
        Document.__init__(self)
        self.add("$out", documentname)


