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
			pass
		elif d['C'][i] == 1:
			tkf1.append(d['TimeUS'][i])
			pn1.append(d['PN'][i])
			pe1.append(d['PE'][i])
			pd1.append(d['PD'][i])
			pn0.append(d['VN'][i])
			pe0.append(d['VE'][i])
			pd0.append(d['VD'][i])

	return tkf1,pn1,pe1,pd1,pn0,pe0,pd0
	
def resizer(ref_arr, data_arr):
	New_Power = interp.interp1d(np.arange(len(data_arr)),data_arr)
	pp = New_Power(np.linspace(0,len(ref_arr)-1,len(ref_arr)))
	return pp
	
if __name__ == '__main__':

	file_name = 'pd.log'
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
	t,px,py,pz,vx,vy,vz = split_dict(xkf1, 'C')
	latitude = px#analysis.Data['GPS']['Lat'][1:]
	longitude = py#analysis.Data['GPS']['Lng'][1:]
	altitude = pz#analysis.Data['GPS']['Alt'][1:]
	time = t
	distance = 0
	d =[]
	d.append(0)
	Velocity = []
	Velocity.append(0)
	for i in range(0,len(t) - 1):
		distance += np.sqrt((px[i+1]-px[i])**2 + (py[i+1]-py[i])**2 )
		d.append(distance)
		Velocity.append(np.sqrt(vx[i]**2 + vy[i]**2))
	pp = np.asarray(resizer(px,Power))
	plt.plot(time,Velocity,label='velocity')
	plt.plot(time,pp,label='vertical speed')
	print(max(Velocity))
	#plt.plot(time,d)
	plt.legend()
	plt.show()