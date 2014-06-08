__author__ = 'civi'


class Document:

    def __init__(self):
        self.doc = {}

    def add(self, key, value):
        if isinstance(value, Document):
            value = value.doc
        self.doc[key] = value

    def __str__(self):
        return str(self.doc)

    def getdoc(self):
        return self.doc
