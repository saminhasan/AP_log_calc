from LogFileStructure import *
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import cm
import numpy as np
from collections import defaultdict
import scipy.interpolate as interp
from FileProcessing import *
def split_dict(d, key):
	tkf0,kf0,pn0,pe0,pd0 = [],[],[],[], []
	tkf1,kf1,pn1,pe1,pd1 = [],[],[],[], []

	for i in range(len(d['TimeUS'])):
		if d['C'][i] == 0:
			tkf0.append(d['TimeUS'][i])
			kf0.append(d['VN'][i])
			pn0.append(d['PN'][i])
			pe0.append(d['PE'][i])
			pd0.append(-d['PD'][i])
		elif d['C'][i] == 1:
			tkf1.append(d['TimeUS'][i])
			kf1.append(d['GZ'][i])
			pn1.append(d['PN'][i])
			pe1.append(d['PE'][i])
			pd1.append(d['PD'][i])

	return tkf0,kf0,tkf1,kf1,pn1,pe1,pd1
	
def resizer(ref_arr, data_arr):
	New_Power = interp.interp1d(np.arange(len(data_arr)),data_arr)
	pp = New_Power(np.linspace(0,len(ref_arr)-1,len(ref_arr)))
	return pp
	
if __name__ == '__main__':

	file_name = 'tf.log'
	lf = LogFile(file_name)
	data = lf.extract_data()
	Voltage = data['BAT']['Volt'][1:]
	Current = data['BAT']['Curr'][1:]
	Time = data['BAT']['TimeUS'][1:]
	Power = np.array([Voltage[i] * Current[i] for i in range(len(Voltage))])
	#plt.plot(data['BAT']['TimeUS'][1:], Voltage, label ='Voltage (V)')
	#plt.plot(data['BAT']['TimeUS'][1:], Current, label ='Current (A)')
	#plt.plot(data['BAT']['TimeUS'][1:], Power/20, label ='Power (W)')


	xkf1 = data['XKF1']
	a,b,c,d,u,v,w = split_dict(xkf1, 'C')
	latitude = u#analysis.Data['GPS']['Lat'][1:]
	longitude = v#analysis.Data['GPS']['Lng'][1:]
	altitude = w#analysis.Data['GPS']['Alt'][1:]
	time = a
	distance = 0
	d =[]
	d.append(0)
	for i in range(0,len(a) - 1):
		distance += np.sqrt((u[i+1]-u[i])**2 + (v[i+1]-v[i])**2 )
		d.append(distance)

	plt.plot(time,d,label='distance')
	print(distance)
	#plt.plot(time,d)
	plt.legend()
	plt.show()