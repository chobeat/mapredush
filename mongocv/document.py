__author__ = 'civi'


class Document:

    def __init__(self):
        self.query = {}

    def add(self, key, value):
        if isinstance(value, Document):
            value = value.query
        self.query[key] = value

    def __str__(self):
        return str(self.query)

