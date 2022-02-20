from LogFileStructure import *
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


class LogFile:
	def __init__(self, filename):
		self.filename = filename
		self.log_data = LogDict
		self.logger_msgs = LogDict.keys()

	def extract_data(self):
		log_file = open(self.filename, 'r')
		for Line in log_file:
			line = Line.rstrip().split(',')

			if line[0] in self.logger_msgs:
				for Field in self.log_data[line[0]].keys():
					line_index = self.log_data[line[0]][Field][0]
					try:
						if line[line_index] == 'NaN':
							pass
						else:
							self.log_data[line[0]][Field].append(float(line[line_index]))

					except Exception as e:
						print(self.log_data[line[0]][Field], line,line_index)
						print(e)
						exit()

			else:	
				pass
		log_file.close()
		return self.log_data 
		
def split_d(d, key):
	tkf0,kf0 = [],[]
	tkf1,kf1 = [],[]

	for i in range(len(d['TimeUS'])):
		if d['C'][i] == 0:
			tkf0.append(d['TimeUS'][i])
			kf0.append(d['GZ'][i])
		elif d['C'][i] == 1:
			tkf1.append(d['TimeUS'][i])
			kf1.append(d['GZ'][i])

	return tkf0,kf0,tkf1,kf1

if __name__ == '__main__':

	file_name = 'ff.log'
	lf = LogFile(file_name)
	data = lf.extract_data()
	xkf1 = data['XKF1']
	x,y,a,b = split_d(xkf1, 'C')
	#plt.plot(xkf10['TimeUS'][1:], xkf10['GZ'][1:])
	#plt.plot(xkf10['TimeUS'][1:], xkf10['GZ'][1:])
	plt.plot(x,y, 'b')
	plt.plot(a,b, 'g')
	plt.show()