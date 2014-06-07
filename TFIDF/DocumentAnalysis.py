#Civi e Andre
import re, math
from collections import Counter
import string
#Rappresenta un singolo documento
class Document:


    #TODO migliorare la regex
    #Costruttore, crea il dizionario delle parole di un testo, crea il dizionario delle occorrenze e delle frequenze
    def __init__(self, doc):
        self.doc = doc
        self.freqDict = dict()

        #tempList = re.findall("([a-z]+)", doc.lower())
	valid_chars = " %s%s" % (string.ascii_letters, string.digits)
        doc=''.join(c for c in doc if c in valid_chars)
        tempList=doc.split(" ")

        self.nwords = float(len(tempList))

        for word in tempList:
            if word not in self.freqDict:
                self.freqDict[word] = tempList.count(word)/self.nwords

        self.wordsVector = Counter(tempList)



    #Restituisce il dizionario delle frequenze
    def getfreqDict(self):
        return self.freqDict

    #Se una parola e' presente nel testo
    def contains(self, word):
        return word in self.freqDict

      #Restituisce il vettore del conteggio delle parole
    def getVectorFromList(self):
        return self.wordsVector



#Rappresenta l'analizzatore di piu' documenti
class DocumentAnalysis:

    arrayDoc = []

    #Il costruttore appende il primo documento
    def __init__(self, doc=[]):
        if isinstance(doc,list):
		for i in doc:
			self.appendDocument(i)
	else:
		self.appendDocument(doc)

    #Aggiungiamocene di altri
    def appendDocument(self, doc):
        self.arrayDoc.append(doc)

    #Calcola IDF
    def InverseDocumentFrequency(self, word):
        counter = 0
        nDocs = self.nDocuments()
        for doc in self.arrayDoc:
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


    def nDocuments(self):
        return len(self.arrayDoc)

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

        diceCoeff = float(num)/den
        try:
            return diceCoeff
        except Exception:
            print "diceCoefficient: return Error"


#PROVE VARIE
doc1 = Document("essere o nonessere?")
doc2 = Document("cosa vuol dire nonessere? essere mah nel dubbio #gazzurbo")


analysis = DocumentAnalysis(doc1)
analysis.appendDocument(doc2)
vector1 = doc1.getVectorFromList()
vector2 = doc2.getVectorFromList()


print doc1.doc

print doc2.doc


print "IDF: " + str(analysis.InverseDocumentFrequency("essere"))

cosSim = analysis.cosineSimilarity(vector1, vector2)
print "CosSim: " + str(cosSim)

diceCoeff = analysis.diceCoefficient(vector1, vector2)
print "DiceCoeff: " + str(diceCoeff)

