from compositequerydocument import CompositeQueryDocument

__author__ = 'civi'

class AndDocument(CompositeQueryDocument):
    def __init__(self, list):
        CompositeQueryDocument.__init__(self,"$and",list)