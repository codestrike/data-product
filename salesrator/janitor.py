import pandas as pd
import numpy as np

#Get Missing Values if Replace_by empty Delete 
def missing_value(frame,cols=None,replace_by=None):
	
	if replace_by==None:
		if cols==None:
			frame.dropna(inplace=True)
		else:
			frame.dropna(inplace=True,subset=[col])
	else:
		
		if type(cols) is None:
			for i in frame.columns:
				frame[i]=frame[i].apply(lambda x:(replace_by if pd.isnull(x) else x))
				

		else:
			for col in cols:
				frame[col]=frame[col].apply(lambda x:(replace_by if pd.isnull(x) else x))
			
					

def replace_value(frame,to_replace,col,replace_by=None):
	no_rows = frame.shape[0]
	if replace_by==None:
		indices= frame.index[frame[col]]
		frame.drop(indices,inplace=True)
	else:
		frame[col]=frame[col].apply(lambda x:(replace_by if x==to_replace else x))
		'''for i in frame.index:
			if frame[col][i]==to_replace:
				frame.ix[i,col]=replace_by'''
		
def replace_non_number(frame,cols,replace_by=None,to_int=True):
	#print frame.shape
	no_rows = frame.shape[0]
	for col in cols:
		for i in frame.index:
			try:
				if to_int:
					temp = int(frame[col][i]) 
				else:
					temp = float(frame[col][i])
			except ValueError:
				if replace_by==None:
					frame.drop([i],inplace=True)
				else:
					frame.ix[i,col]=replace_by


			

def replace_negative(frame,col,delete=False,replace_by=None):
	floor(frame,col,0,delete,replace_by)
	'''if delete==False:
		for i in frame.index:
			if frame.ix[i,col]<0:
				frame.ix[i,col]=replace_by'''



def to_upper(frame,col):
	frame[col]=frame[col].apply(lambda x:x.upper())
	


def to_lower(frame,col):
	frame[col]=frame[col].apply(lambda x:x.lower())

def strip_left_right(frame,col):
	no_rows = frame.shape[0]
	for i in frame.index:
		frame.ix[i,col] = frame.ix[i,col].strip()


def slice_string(frame,col,number=3):
	no_rows = frame.shape[0]
	for i in frame.index:
		frame.ix[i,col] = frame.ix[i,col][0:number]
		

	
def floor(frame,col,floor,delete=True,replace_by=None):
	no_rows = frame.shape[0]
	if delete:
		indices= frame.index[frame[col]<floor]
		frame.drop(indices,inplace=True)
	else:
		for i in frame.index:
			
			if frame.ix[i,col]<floor:
				if replace_by==None:
					frame.ix[i,col]=floor
				else:
					frame.ix[i,col]=replace_by
					
def cap(frame,col,cap,delete=True,replace_by=None):
	no_rows = frame.shape[0]
	if delete:
		indices= frame.index[frame[col]>cap]
		frame.drop(indices,inplace=True)
	else:
		for i in frame.index:
			if frame.ix[i,col]>cap:
				if replace_by==None:
					frame.ix[i,col]=cap
					#print frame.ix[i,col]
				else:
					frame.ix[i,col]=replace_by


def convert_to_float(frame,cols):
	no_rows = frame.shape[0]
	for col in cols:
		frame[col]= frame[col].astype(float)

def convert_to_int(frame,cols):
	for col in cols:
		frame[col]= frame[col].astype(int)

def string_to_float(frame,cols=None):
	
	if type(cols) is not list:
		cols=frame.columns
	for col in cols:
		for i in frame.index:
			if type(frame.ix[i,col]) is str:
				#print frame.ix[i,col]
				frame.ix[i,col]=float(frame.ix[i,col].replace(',',''))
				#print frame.ix[i,col]

def convert_to_category(frame,cols):
	for col in cols:
		frame[col]= frame[col].astype("category")

def string_to_int(frame,cols=None):
	if type(cols) is None:
		cols=frame.columns
	for col in cols:
		for i in frame.index:

			frame.ix[i,col]=int(frame.ix[i,col].replace(',',''))

def remove_lower_outlier(frame,col,lower=None):
	if(lower==None):
		lower=frame[col].mean()-3*frame[col].std()
	for i in frame.index:
		if frame.ix[i,col]<lower:
				frame.drop(i,inplace=True)


def remove_higher_outlier(frame,col,higher=None):
	if(higher==None):
		higher=frame[col].mean()+3*frame[col].std()
	for i in frame.index:
		if frame.ix[i,col]>higher:
				frame.drop(i,inplace=True)
	



def delete_col(frame,group_cols):
	columns=frame.columns
	for col in group_cols:
		if col in columns:
			del frame[col]