from pandas import DataFrame
import reader
class cube:

	def __init__(self,framedict):
		self.data=framedict

	def aggregate(self):
		cube_frame = DataFrame()
		values = self.data.keys()
		for i in values:
			cube_frame=cube_frame.add(self.data[i],fill_value=0)

		return cube_frame

	def row_add(self):
		
		temp_dict={}
		for i in self.data.keys():
			temp_dict[i]=self.data[i].sum(axis=0)
		cube_frame = DataFrame(temp_dict)
		return cube_frame

	def column_add(self):
		temp_dict={}
		for i in self.data.keys():
			temp_dict[i]=self.data[i].sum(axis=1)
		cube_frame = DataFrame(temp_dict)
		return cube_frame

	def slice(self,rows,columns,keys,inplace=False):
		framedict={}

		for i in keys:
			framedict[i]=self.data[i].ix[rows,columns]
		if (inplace):
			self.data = framedict
		else:
			newcube=cube(framedict)
			return newcube