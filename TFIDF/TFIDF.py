from ghost import Ghost
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from pymongo import MongoClient
from bson.code import Code
import logging
import re
import string

#Trasforma un documento in un dizionario di occorrenze delle parole presente. Fa una sanitizzazione della punteggiatura ma non toglie stop words
def docToTF(doc):
	valid_chars = " %s%s" % (string.ascii_letters, string.digits)
	doc=''.join(c for c in doc if c in valid_chars)
	words=doc.split(" ")
	TF={}
	for word in words:
		TF[word]=TF.setdefault(word,0)+1
	return TF

def TFmap1(textField):
	func=Code("""function(){
		words=this."""+textField+""".split(' ')

		for(i=0;i<words.length;i++){
		word=words[i]
		if(word.length>2){

		emit({doc:this._id,w:word},1)}
		}
		}
		""")
	return func

def TFreduce1():
	func=Code("""function(k,values){
		return Array.sum(values)

}""")
	return func

def TFmap2():
	func=Code("""function(){

		emit(this._id.doc,{word:this._id.w,val:this.value})

		}
		""")
	return func



def TFreduce2():
	func=Code("""function(doc,values){
		res=""
		for(k in values){
		res+=values[k].word+":"+values[k].val+";"
		}
		return res

	}""")
	return func

if __name__=="__main__":
	client=MongoClient()
	db=client.test
	cars=db.cars
	#cars.map_reduce(TFmap1("_id"),TFreduce1(),"resultTF1")

	resultTF=db.resultTF1
	resultTF.map_reduce(TFmap2(),TFreduce2(),"resultTF2")
