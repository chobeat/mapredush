#Civi e Andre
import re, math
from collections import Counter

import string
#from faker import *
import pprint
from multiprocessing import Pool
from functools import partial
from itertools import combinations
#Rappresenta un singolo documento


def getkgrams(word, k):
    return set([word[i:i+k] for i in range(len(word)-k+1)])


def exactWordInCommon(setDoc1, setDoc2):
    return set(setDoc1.keys()) & set(setDoc2.keys())


def kgramswordssimilarity(word1, word2, k):
    k1 = getkgrams(word1, k)
    k2 = getkgrams(word2, k)

    num = len(k1 & k2)
    den = len(k1 | k2)
    try:
        return float(num)/den
    except ZeroDivisionError:
        return 0

def kgramsimilarity(setDoc1, setDoc2, k, threshold):
    res = set()
    for word1 in setDoc1:
        for word2 in setDoc2:
            if kgramswordssimilarity(word1, word2, k) >= threshold:
                res.add(word1)
                res.add(word2)
    return res


#Calcola la CosSim a partire da due vettori di occorrenze di parole
def cosineSimilarity(setDoc1, setDoc2):

        #Considero le parole in comune
        wordsInCommon = exactWordInCommon(setDoc1, setDoc2)

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
def diceCoefficient(setDoc1, setDoc2):

    wordsInCommon = exactWordInCommon(setDoc1, setDoc2)

    num = len(wordsInCommon)
    den = len(setDoc1)+len(setDoc2)

    try:
        diceCoeff = 2*(float(num)/den)
        return diceCoeff
    except Exception:
        return 0

def diceKgramCoefficient(setDoc1, setDoc2, k, threshold):

    num = 0
    tmp = dict()

    for word1 in setDoc1:
        for word2 in setDoc2:
            if kgramswordssimilarity(word1, word2, k) >= threshold:
                try:
                    tmp[(word1, word2)]
                except KeyError:
                    num += 1
                    tmp[(word1, word2)] = None
                    tmp[(word2, word1)] = None



    den = len(setDoc1)+len(setDoc2)

    try:
        diceCoeff = 2*(float(num)/den)
        return diceCoeff
    except Exception:
        return 0

class TextDocument:

    #TODO migliorare la regex
    #Costruttore, crea il dizionario delle parole di un testo, crea il dizionario delle occorrenze e delle frequenze
    def __init__(self, doc):
        self.doc = doc
        self.freqDict = dict()
        self.wordsVector = dict()

        #tempList = re.findall("([a-z]+)", doc.lower())

        tempList = re.findall(r"(\w+)", doc.lower())

        #valid_chars = " %s%s" % (string.ascii_letters, string.digits)
        #doc = ''.join(c.lower() for c in doc if c in valid_chars)
        #tempList = doc.split(" ")

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
        return word in self.wordsVector

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


        self.allWords=self.getAllWords()


    #Calcola IDF
    def InverseDocumentFrequency(self, word):
        counter = 0
        nDocs = len(self)

        for document in self:
            if document.contains(word):
                counter += 1
        try:
            return float(nDocs) / counter
        except ZeroDivisionError:
            return 0

    #Calcola TFIDF
    def TFIDF(self, tf, word):
        return tf * self.InverseDocumentFrequency(word)

    def getAllWords(self):

        return set([word for doc in self for word in doc.getVector()])

    def getIDFxWord(self):
        return {word:self.InverseDocumentFrequency(word) for word in self.getAllWords()}

    def getAllTFIDF(self):
        return {i: sorted([(word, self.TFIDF(self[i].getTF(word), word)) for word in self[i].getVector()],key=lambda x:x[1],reverse=True) for i in range(len(self))}

    def getDiceKGramSimilarityMatrix(self, *args,**kwargs):
        return self.getSimilarityMatrix(diceKgramCoefficient, *args,**kwargs)

    def getDiceSimilarityMatrix(self, *args,**kwargs):
         return self.getSimilarityMatrix(diceCoefficient, *args,**kwargs)

    def getCosineSimilarityMatrix(self, *args,**kwargs):
        return self.getSimilarityMatrix(cosineSimilarity, *args,**kwargs)

    def getSimilarityMatrix(self, f, *args, **kwargs):
        couples = combinations(range(len(self)), 2)
        return [(i, j, f(self[i].getVector(), self[j].getVector(),*args,**kwargs)) for i, j in couples]



"""
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
        den = len(setDoc1)+len(setDoc2)

 	diceCoeff = 2*(float(num)/den)
        try:
            return diceCoeff
        except Exception:
            print "diceCoefficient: return Error"
"""


"""
text1 = "I piselli me li mangio per intero."
text2 = "Spisellami sta fava, mangiateli tu! Integro."
doc1 = TextDocument(text1)
doc2 = TextDocument(text2)

print diceCoefficient(doc1.wordsVector, doc2.wordsVector, kgramsimilarity, 2, 0.4)
"""

"""
lst = DocumentAnalysis([doc1, doc2, doc3])
lst.InverseDocumentFrequency("essere")
"""



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
from faker import Faker
faker=Faker()
pp=pprint.PrettyPrinter(indent=4)

import time
t0=time.time()
analysis=DocumentAnalysis([TextDocument(faker.text(140)) for i in range(100)])
print analysis.getDiceKGramSimilarityMatrix(2,0.4)
t1=time.time()
print t1-t0
#pp.pprint(analysis.getCosineSimilarityMatrix())
"""

