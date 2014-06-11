from compositequerydocument import CompositeQueryDocument

__author__ = 'civi'

class OrDocument(CompositeQueryDocument):
    def __init__(self, list):
        CompositeQueryDocument.__init__(self,"$or",list)