__author__ = 'civi'


class Document:

    def __init__(self):
        self.doc = dict()

    def add(self, key, value):
        if isinstance(value, Document):
            value = value.getdoc()
        self.doc[key] = value

    def __str__(self):
        return str(self.doc)

    def getdoc(self):
        return self.doc


