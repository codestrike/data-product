import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from itertools import cycle
from sklearn.cluster import k_means,KMeans,Ward
from sklearn.decomposition import PCA
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler


#Cluster Generation K-Mean
def k_mean(frame,cluster_no,X):
	#X=['EQUITY.AUM','GOLD.AUM','LIQUID.AUM','DEBT.AUM']
	#cls = fit(X,Y)#['TOTAL.AUM'])
	kmeans = KMeans(init='k-means++', n_clusters=cluster_no, n_init=10)
	kmeans.fit(frame.ix[:,X])
	#print kmeans.cluster_centers_
	return kmeans



#Plotting Cluster based on k-mean 
def plot(kmeans,frame,factors,filename,axes=(0,1)):
	xaxis=axes[0]
	yaxis=axes[1]	
	centers = kmeans.cluster_centers_
	print centers

	labels = kmeans.predict(frame[factors])
	X=frame.as_matrix(factors)
	# Number of clusters in labels, ignoring noise if present.
	n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
		

	##############################################################################
	# Plot result
	# Black removed and is used for noise instead.
	unique_labels = set(labels)
	colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
	for k, col in zip(unique_labels, colors):
		if k == -1:
	        # Black used for noise.
			col = 'k'
		class_member_mask = (labels == k)
		xy = X[class_member_mask]
		plt.plot(xy[:, xaxis], xy[:, yaxis], 'o', markerfacecolor=col,markeredgecolor='k', markersize=6)
	for center in centers:
		plt.plot(center[xaxis],center[yaxis],'x',markerfacecolor='k',markeredgecolor='k',markersize=24)
	plt.title('Estimated number of clusters: %d' % n_clusters_)
	plt.savefig(filename)

	#plot to a jpeg img

