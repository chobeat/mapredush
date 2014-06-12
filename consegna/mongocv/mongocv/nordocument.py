from compositequerydocument import CompositeQueryDocument

__author__ = 'civi'

class NorDocument(CompositeQueryDocument):
    def __init__(self, list):
        CompositeQueryDocument.__init__(self,"$nor",list)