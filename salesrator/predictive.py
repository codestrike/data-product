import pandas as pd
import numpy as np
import Orange,reader
import pydot

from sklearn.feature_extraction import DictVectorizer as DV
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction import FeatureHasher as FH
from StringIO import StringIO
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree as sktree
'''
enc=OneHotEncoder()
fh=FH(input_type="string")
t=fh.fit_transform([['a','b'],['b','c']])
print t.n_values_'''

def orange_tree(frame,x,y):
	X=frame.ix[:,x]
	Y=frame.ix[:,y]
	Z=X.append(Y)
	t = reader.df2table(Z)
	#t.save("output_W3.tab") #table
	otree = Orange.classification.tree.TreeLearner(t,min_subset=1000)
	return otree

def plot_orange_tree(otree):
	otree.dot(file_name="output_W3.dot", node_shape="ellipse", leaf_shape="box")
	

def sklearn_tree(frame,x,y):
	vectorize = DV(sparse=False)
	X=frame.ix[:,x]
	Y=frame.ix[:,y]
	del frame
	X_transform = vectorize.fit_transform(X.to_dict(outtype="records"))
	dtree = sktree.DecisionTreeRegressor(max_depth=10,min_samples_split=2000)
	dtree = dtree.fit(X_transform,Y)
	return dtree


def plot_tree(dtree,fname):
	if type(dtree) is DecisionTreeRegressor:
		dot_data = StringIO()
		tree.export_graphviz(dtree,out_file=dot_data)
		graph = pydot.graph_from_dot_data(dot_data.getvalue())
		graph.write_pdf(fname)
	elif type(dtree) is Orange.classification.tree.TreeClassifier:
		dtree.dot(file_name=fname, node_shape="ellipse", leaf_shape="box")
	else:
		pass


def predict(frame,dtree,xfactors=None):

	
	if type(dtree) is DecisionTreeRegressor:
		
		if (xfactors==None):
			y=dtree.predict(frame)
		else:
			y=dtree.predict(frame[xfactors])
		return y

	elif type(dtree) is Orange.classification.tree.TreeClassifier:
		#print type(frame[xfactors])
		#print list(frame[xfactors].iloc[0])
		t = (reader.df2table(frame[xfactors]))
		#domain = t.domain
		#print type(domain)
		inst = t[0]#Orange.data.Instance(t)
		print (inst)
		y = dtree.descender(inst)
		'''res=Orange.evaluation.testing.cross_validation(tree,frame[xfactors])
		CAs = Orange.evaluation.scoring.CA(res)
		AUCs = Orange.evaluation.scoring.AUC(res)
		print CAs
		y=(CAs,AUCs)'''
		return y
	else:
		pass

