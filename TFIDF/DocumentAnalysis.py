#Civi e Andre
import re, math
from collections import Counter
from reportlab.lib.xmllib import TestXMLParser
import string
#from faker import *
import pprint
from multiprocessing import Pool
from functools import partial
#Rappresenta un singolo documento


class TextDocument:

    #TODO migliorare la regex
    #Costruttore, crea il dizionario delle parole di un testo, crea il dizionario delle occorrenze e delle frequenze
    def __init__(self, doc):
        self.doc = doc
        self.freqDict = dict()
        self.wordsVector = dict()

        #tempList = re.findall("([a-z]+)", doc.lower())

        valid_chars = " %s%s" % (string.ascii_letters, string.digits)
        doc = ''.join(c.lower() for c in doc if c in valid_chars)
        tempList = doc.split(" ")

        self.nwords = len(tempList)

        self.wordsVector = Counter(tempList)

        self.freqDict = {word: self.wordsVector[word]/float(self.nwords) for word in self.wordsVector}


    #Restituisce il dizionario delle frequenze
    def getfreqDict(self):
        return self.freqDict

    def getTF(self, word):
        return self.freqDict[word]

    #Se una parola e' presente nel testo
    def contains(self, word):
        return word in self.freqDict

      #Restituisce il vettore del conteggio delle parole
    def getVector(self):
        return self.wordsVector


#Rappresenta l'analizzatore di piu' documenti
class DocumentAnalysis(list):

    #Il costruttore appende il primo documento
    def __init__(self, doc=[]):

        if isinstance(doc, list):
            for i in doc:
                self.append(i)
        else:
            self.append(doc)

    #Calcola IDF
    def InverseDocumentFrequency(self, word):
        counter = 0
        nDocs = len(self)
        for doc in self:

            if doc.contains(word):
                counter += 1
        ''' DEBUG
        print "nDocs: " + str(nDocs)
        print "counter: " + str(counter)
        '''

        try:
            return float(nDocs / counter)
        except ZeroDivisionError:
            return 0

    #Calcola TFIDF
    def TFIDF(self, tf, word):
        return tf * self.InverseDocumentFrequency(word)

    def getAllWords(self):
        return set([word for doc in self for word in doc.getVector()])

    def getIDFxWord(self):
        return {word:self.InverseDocumentFrequency(word)   for word in self.getAllWords()}

    def getAllTFIDF(self):
        return {doc: sorted([(word,self.TFIDF(doc.getTF(word),word)) for word in doc.getVector()],key=lambda x:x[1],reverse=True) for doc in self }


    #Calcola la CosSim a partire da due vettori di occorrenze di parole
    def cosineSimilarity(self, setDoc1, setDoc2):

        #Considero le parole in comune
        wordsInCommon = set(setDoc1.keys()) & set(setDoc2.keys())
        num = sum([setDoc1[value] * setDoc2[value] for value in wordsInCommon])

        #somme al quadrato
        sumDoc1 = sum([math.pow(setDoc1[value], 2) for value in setDoc1.keys()])
        sumDoc2 = sum([math.pow(setDoc2[value], 2) for value in setDoc2.keys()])
        den = math.sqrt(sumDoc1) * math.sqrt(sumDoc2)

        try:
            return float(num) / den
        except Exception:
            return 0.0

    #Calcola la dice Coefficent a partire da due vettori di occorrenze di parole
    #In sostanza sono i termini matchanti fra 2 documenti
    def diceCoefficient(self, setDoc1, setDoc2):
        wordsInCommon = set(setDoc1.keys()) & set(setDoc2.keys())
        num = len(wordsInCommon)
        lenDoc1 = sum([value for value in setDoc1.values()])
        lenDoc2 = sum([value for value in setDoc2.values()])
        den = lenDoc1+lenDoc2

        ''' debug
        print "len1 " + str(lenDoc1)
        print "len2 " + str(lenDoc2)
        print "num " + str(num)
        print "den " + str(den)
        '''

        diceCoeff = 2*(float(num)/den)
        try:
            return diceCoeff
        except Exception:
            print "diceCoefficient: return Error"

    def getSimilarityMatrix(self,f,sortByAff=True):
        return  [(pos,self.getSimilarityVector(pos,f,sortByAff)) for pos in range(len(self))]

    def getSimilarityVector(self,currPos,f,sortByAff=True):
        curr=self[currPos]
        k= 1 if sortByAff else 0
        return sorted([(pos,f(curr.getVector(),self[pos].getVector())) for pos in range(len(self)) if pos!=currPos],key=lambda x:x[k],reverse=True)

    def getDiceSimilarityMatrix(self):
        return self.getSimilarityMatrix(self.diceCoefficient)

    def getCosineSimilarityMatrix(self):
        return self.getSimilarityMatrix(self.cosineSimilarity)


text = "Non voglio essere capito. Voglio essere, capito?"
doc = TextDocument(text)




'''

#PROVE VARIE
doc1 = TextDocument("essere, essere o nonessere?")
doc2 = TextDocument("cosa vuol dire nonessere? essere mah nel dubbio #gazzurbo")
vector1=doc1.getVector()
vector2=doc2.getVector()
analysis = DocumentAnalysis(doc1)
analysis.append(doc2)

print analysis.getDiceSimilarityMatrix()

print "IDF: " + str(analysis.InverseDocumentFrequency("essere"))

cosSim = analysis.cosineSimilarity(vector1, vector2)
print "CosSim: " + str(cosSim)

diceCoeff = analysis.diceCoefficient(vector1, vector2)
print "DiceCoeff: " + str(diceCoeff)
'''
"""
faker=Faker()
pp=pprint.PrettyPrinter(indent=4)

import time
t0=time.time()
analysis=DocumentAnalysis([Document(faker.text(140)) for i in range(1000)])
analysis.getDiceSimilarityMatrix()

t1=time.time()
print t1-t0
#pp.pprint(analysis.getCosineSimilarityMatrix())
"""