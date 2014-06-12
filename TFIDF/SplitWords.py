from ghost import Ghost
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from pymongo import MongoClient
from bson.code import Code
from collections import OrderedDict
import mongocv
import logging
import re
import string
import json
def splitMap():
        func=Code("""function(){
                words=this.text.split(/\W+/g)

                for(i=0;i<words.length;i++){
                word=words[i]
                if(word.length>2){

                emit(word.toLowerCase(),1)
                }
                }}
                """)
        return func

def splitReduce():
        func=Code("""function(key,values){
	return key
}
                """)
        return func




if __name__=="__main__":
	"""
        client=MongoClient()
        db=client.db
        tc=db.textCollection
	s=set()

        tc.map_reduce(splitMap(),splitReduce(),"resultSplit")
	"""
	print dir(mongocv)
