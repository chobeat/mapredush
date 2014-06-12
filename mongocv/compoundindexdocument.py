from document import Document
from collections import OrderedDict
import json

__author__ = 'Francesco'

'''
Un indice è ordinato di default in maniera ascendete su un certo campo. Per pecificare
l'ordine discendente si aggiunge '_' come radice del nome del campo
'''
class CompoundIndex:

    def __init__(self):
        self.insidedoc = OrderedDict()

    def __init__(self, list):
        self.insidedoc = OrderedDict()
        self.addListIndex(list)

    def __init__(self, field):
        self.insidedoc = OrderedDict()
        if field.startswith('_'):
            self.addDescIndex(field)
        else:
            self.addIndex(field)

    def addDescIndex(self, field):
        self.insidedoc.__setitem__(field, -1)

    def addIndex(self, field):
        self.insidedoc.__setitem__(field, 1)

    def addListIndex(self, list):
         for x in list:
            if x.startswith('_'):
                self.insidedoc.__setitem__(x.split('_', 1)[1], -1)
            else:
                self.insidedoc.__setitem__(x, 1)

    def removeIndex(self, field):
        self.insidedoc.pop(field)

    def __str__(self):
        return json.dumps(self.insidedoc)


i = CompoundIndex(['_mannaggia', '_marca', 'anno', '_ciccio'])
print i
i.removeIndex('marca')
print i