import sys
from .reader import *
import cPickle as pickle
import datetime
import time
import os
import shutil
# import janitor


class A3_lib:
	def a3_add(self,filename, base_dir):
		csv_file = readcsv(filename,index_col=None)	
		# print b
		if not os.path.exists(base_dir):
			os.makedirs(base_dir)
		base_dir=os.path.join(base_dir,int(time.time()))
		pickle.dump(csv_file,open(base_dir,"wb"))

		
	def a3_read(self,userid,base_dir):
		filepath=os.path.join(base_dir,userid)
		if os.path.exists(filepath):
			try :	
				lastest_file = max(os.listdir(filepath))
				pickle_file = pickle.load(open(os.path.join(filepath,lastest_file),"rb"))
				return pickle_file

			except ValueError:
				print "File does not exists"
		else:
			print "Invaid UserId"


	def a3_write(self,filename,userid,base_dir):
		filepath = os.path.join(base_dir,userid)
		if os.path.exists(filepath):
			try:
				lastest_file = max(os.listdir(filepath))
				filepath = os.path.join(filepath,str(lastest_file))
				pickle_file = pickle.dump(filename,open(filepath,"wb"))
				return pickle_file
			except ValueError:
				print "Some thing is wrong"
		else:
			print "Invalid UserId"




	def a3_remove(self,base_dir,userid):
		shutil.rmtree(os.path.join(base_dir,userid))