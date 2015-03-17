import pandas as pd

#Returns the Data-Types of Each Column in the DataFrame.
def data_types(frame):
	d_frame = frame.dtypes
	return d_frame

#Returns Data for Each Column of DataFrame in form of count,mean,std,min,max,25%,50%,75%
def describe_numeric(frame):
	print "here"
	return frame.describe(include=['number'])

#Returns Data for Each Column of DataFrame in form of count,unique,top,mean,min,max,freq,25%,50%,75%
def describe_all(frame):
	# return frame.describe(include=['all'])
	return frame.describe()


#Returns Data from DataFrame if any Column present in Categorial Format
def describe_categorical(frame):
	return frame.describe(include=['category'])

#Returns All Unique Values of the Column Passed along with the DataFrame.
def get_unique_vals(frame,col):
	return frame[col].unique()
	
#Returns Outliers for Each Column of DataFrame in form of lower_outliers,higher_outliers,num_negative,num_null
def num_outliers(frame):
	no_rows=frame.shape[0]
	df=pd.DataFrame()
	for col in frame.columns:
		if (frame[col].dtype==float or frame[col].dtype==int):
			lower=(frame[col][frame[col]<frame[col].mean()-3*frame[col].std()]).count()
			higher=(frame[col][frame[col]>frame[col].mean()+3*frame[col].std()]).count()
			numnegative=(frame[col][frame[col]<0]).count()
			numnull=no_rows-frame[col].count()
			df.ix['lower_outliers',col]=lower
			df.ix['higher_outliers',col]=higher
			df.ix['num_negative',col]=numnegative
			df.ix['num_null',col]=numnull
	return df