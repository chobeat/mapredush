#Civi e Andre
import re, math
from collections import Counter
import string
#from faker import *
import pprint
from multiprocessing import Pool
from functools import partial
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
        print wordsInCommon

        print setDoc1
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
def diceCoefficient(setDoc1, setDoc2, similarityfunction, *args):

    wordsInCommon = similarityfunction(setDoc1, setDoc2, *args)
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
        return {word:self.InverseDocumentFrequency(word)   for word in self.getAllWords()}

    def getAllTFIDF(self):
        return {doc: sorted([(word, self.TFIDF(doc.getTF(word), word)) for word in doc.getVector()],key=lambda x:x[1],reverse=True) for doc in self }

    def getSimilarityMatrix(self,f,sortByAff=True):
        return  [(pos,self.getSimilarityVector(pos,f,sortByAff)) for pos in range(len(self))]

    def getSimilarityVector(self,currPos,f,sortByAff=True):
        curr=self[currPos]
        k= 1 if sortByAff else 0
        return sorted([(pos,f(curr.getVector(),self[pos].getVector())) for pos in range(len(self)) if pos!=currPos],key=lambda x:x[k],reverse=True)

    def getDiceSimilarityMatrix(self):
        return self.getSimilarityMatrix(diceCoefficient)

    def getCosineSimilarityMatrix(self):
        return self.getSimilarityMatrix(cosineSimilarity)




"""
text1 = "I piselli me li mangio per intero."
text2 = "Spisellami sta fava, mangiateli tu! Integro."
doc1 = TextDocument(text1)
doc2 = TextDocument(text2)

print diceCoefficient(doc1.wordsVector, doc2.wordsVector, kgramsimilarity, 3, 0.3)

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
