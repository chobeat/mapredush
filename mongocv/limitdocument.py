from document import Document

__author__ = 'Francesco'

# Classe rappresentante l'operatore 'Limit'
class LimitDocument(Document):

    #Costruisci l'operatore passando il numero di elementi da visualizzare
    def __init__(self, value):
        Document.__init__(self)
        self.add(self, '$limit', value)

