from mongocv import *

from os import listdir
from os.path import isfile,join

onlyfiles = [ f[:-3] for f in listdir("./mongocv") if isfile(join("./mongocv",f)) and f[-3:]==".py" ]

for i in onlyfiles:
	print dir(i)

