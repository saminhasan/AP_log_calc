from LogFileStructure import *
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import cm
import numpy as np
from collections import defaultdict
import scipy.interpolate as interp


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
        
def split_dict(d, key):
    tkf0,kf0,pn0,pe0,pd0 = [],[],[],[], []
    tkf1,kf1,pn1,pe1,pd1 = [],[],[],[], []

    for i in range(len(d['TimeUS'])):
        if d['C'][i] == 0:
            tkf0.append(d['TimeUS'][i])
            kf0.append(d['GZ'][i])
            pn0.append(d['PN'][i])
            pe0.append(d['PE'][i])
            pd0.append(-d['PD'][i])
        elif d['C'][i] == 1:
            tkf1.append(d['TimeUS'][i])
            kf1.append(d['GZ'][i])
            pn1.append(d['PN'][i])
            pe1.append(d['PE'][i])
            pd1.append(d['PD'][i])

    return tkf0,kf0,tkf1,kf1,pn0,pe0,pd0

if __name__ == '__main__':

    file_name = 'tf.log'
    lf = LogFile(file_name)
    data = lf.extract_data()
    Voltage = data['BAT']['Volt'][1:]
    Current = data['BAT']['Curr'][1:]
    Power = np.array([Voltage[i] * Current[i] for i in range(len(Voltage))])
    #plt.plot(data['BAT']['TimeUS'][1:], Voltage, label ='Voltage (V)')
    #plt.plot(data['BAT']['TimeUS'][1:], Current, label ='Current (A)')
    #plt.plot(data['BAT']['TimeUS'][1:], Power/20, label ='Power (W)')


    xkf1 = data['XKF1']
    a,b,c,d,u,v,w = split_dict(xkf1, 'C')
    #plt.plot(u,v, 'b')
    #plt.show()
    #plt.plot(a,b, 'g',label='jeje')
    #plt.legend()
    #plt.show()
     # 3D Plot of flight data
    latitude = u#analysis.Data['GPS']['Lat'][1:]
    longitude = v#analysis.Data['GPS']['Lng'][1:]
    altitude = w#analysis.Data['GPS']['Alt'][1:]
    fig = plt.figure(figsize=(8,6))
    fig.tight_layout()

    ax = plt.subplot(111, projection='3d')
    ax.xaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('white')
    ax.yaxis.pane.fill = False
    ax.yaxis.pane.set_edgecolor('white')
    ax.zaxis.pane.fill = False
    ax.zaxis.pane.set_edgecolor('white')
    ax.grid(False)
    ax.plot(u, v, w)
    
    New_Power = interp.interp1d(np.arange(len(Power)),Power)
    pp = New_Power(np.linspace(0,len(u)-1,len(u)))
    #m = 0
    #for i in range(len(Power)):
    #   New_Power.append(Power[i])
    
    size = [10 * power / max(pp)  for power in pp]
    print(len(size),len(u))
    s = ax.scatter(latitude, longitude, altitude ,s = size, marker = 'o' , c = pp,cmap = cm.jet, linewidths = 0.025,edgecolors = 'k') 
    c_bar = fig.colorbar(s, ax = ax)
    plt.show()
    t1 = np.linspace(0,30,len(Power))
    plt.plot(t1, Power,label = 'referce')
    t2 = np.linspace(0,30,len(pp))
    plt.plot(t2,pp,label = 'interplorated')
    plt.legend()

    plt.show()
