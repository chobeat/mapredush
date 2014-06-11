from DocumentAnalysis import *
from bitstring import *

class BinaryAnalysis(DocumentAnalysis):

     def binaryDice(self,vec1,vec2):

	a=BitArray(vec1)
	b=BitArray(vec2)

	return (2*float((a&b).count(1)))/(a.count(1)+b.count(1))

     def docToBinaryVector(self,doc):
	return  [1 if word in doc.wordsVector else 0 for word in self.allWords]

     def getAllDocumentsInBinary(self):
	return [(i,self.docToBinaryVector(self[i])) for i in range(len(self))]

     def getBinaryDiceMatrix(self):
	l=self.getAllDocumentsInBinary()
	return [(i[0],j[0], self.binaryDice(i[1],j[1])) for i in l for j in l if i[0]!=j[0]]

from faker import *
faker=Faker()
analysis=BinaryAnalysis([TextDocument(faker.text(300)) for i in range(2000)])
import time
t0=time.time()
analysis.getDiceSimilarityMatrix()
t1=time.time()
print t1-t0
