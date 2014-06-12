from faker import *
from pymongo import *

client=MongoClient()
db=client.db
tc=db['textCollection']
f=Faker()
l=[f.text(140) for i in range(1000)]
for i in range(len(l)):

	tc.insert({"_id":i,"text":l[i]})

