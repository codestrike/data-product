import matplotlib
matplotlib.use('Agg')
import pandas as pd
import json
import matplotlib.pyplot as plt

pd.options.display.max_rows= 100000

#Plotting Histograms
def histogram(frame,col,filename=None,bins=10):
	#frame[col].plot(kind='hist')
	frame[col].hist(bins=bins)
	plt.savefig(filename)
	


#Plotting Box-Plots
def box_plot(frame,col,by,filename,ylim=None):
	dict_plot=frame.boxplot(column=col,by=by)
	#if ylim!=None:
	#	plt.ylim(ylim)
	plt.savefig(filename)
	plt.close()
	#return dict_plot



#Describing DataFrame by Mean,Median,Maximum-Value in Column,Minimum-Value in Column and Count.
def group_by(frame,by,group_cols,func):
	if func == 'mean':
		t = frame.groupby(by=by).mean()
	elif func=='median':
		t = frame.groupby(by=by).median()
	elif func == 'max':
		t = frame.groupby(by=by).max()
	elif func == 'min':
		t = frame.groupby(by=by).min()
	elif func == 'count':
		t = frame.groupby(by=by).count()
	else:
		t=None
	t=t[group_cols]
	return t


#Filtering DataFrame by Providing Constraints 
def filter(frame,constraints):
	result=frame
	
	for col in constraints.keys():
		if type(constraints[col])==list:
			result=result[result[col].isin(constraints[col])]

		elif type(constraints[col])==tuple:
			lower=constraints[col][0]
			higher = constraints[col][1]
			result=result[(result[col]>=lower) & (result[col]<=higher)]			
		elif type(constraints[col])==float or int or str:
			result=result[result[col]==constraints[col]]
		else :	
			pass
	return result



'''

def filter(frame,group_cols,constraints):
	result  = frame

	for col in group_cols:
		if type(constraints)==list:
			result = result[result[col]==constraints[col]]

	return result

	'''