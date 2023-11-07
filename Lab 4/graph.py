import numpy as np
import matplotlib.pyplot as plot
from collections import defaultdict

import os
files = [file for file in os.listdir('.') if os.path.splitext(file)[1] == '.npy']

photopeaks = {
  'na22': (511, 1274),
  'mn54': (835,),
  'co60': (1173, 1332),
  'co57': (706, 137),
  'ba133': (437, 382),
  'cs137': (661,),
  'cd109': (203, 260),
}

real_photopeaks = {
  'na22': (511, 1274),
  'mn54': (851,),
  'co60': (1192, 1356),
  'co57': (666,),
  'ba133': (356,),
  'cs137': (675,),
  'cd109': (),
}

edges = []

for file in files:
    data = np.load(file)
    fname = os.path.splitext(file)[0]
    element = fname[:2].capitalize() + '-' + fname[2:]

    plot.figure(figsize=[7.2, 4.8])

    for E in real_photopeaks[fname]:
        plot.axvline(x=E, color='red', linewidth=0.5)
    plot.scatter(data[1], data[0], s=2)
    #print((data[1][1]-data[1][0]))
    #plot.scatter(data[1], -np.cbrt(data[0])*np.gradient(np.gradient(data[0]))/(data[1][1]-data[1][0]), s=1)
    #print(list(data[1]))
    for p in real_photopeaks[fname]:
        MIN = None
        MAX = None
        peaki = np.argmin(abs(data[1]-p))
        i = 0
        while True:
            i += 1
            if MIN is None and data[0][peaki-i] > data[0][peaki-i+1]:
                MIN = data[1][peaki-i+1]
            elif MIN is not None and data[0][peaki-i] < data[0][peaki-i+1]:
                MAX = data[1][peaki-i+1]
                break
        print(MIN, MAX)
        plot.axvline(x=data[1][np.argmin(abs(data[1]-MIN/2-MAX/2))], color='green', linewidth=0.5)

        edges.append((p, data[1][np.argmin(abs(data[1]-MIN/2-MAX/2))]))

    plot.ylabel('Counts')
    plot.xlabel('Energy (keV)')
    #plot.xticks(data[1][data[1]<1500])
    plot.xlim([0, 1500])
    plot.title('Number of Events by Energy (%s)' % element)
    #plot.savefig('images/%s.png' % fname)

#plot.show()
print(edges)
plot.figure(figsize=[7.2, 4.8])
p2m = np.array([(2*e[0] - e[1])**2/1022 for e in edges])
dp2m = np.array([abs(2*(2*e[0] - e[1])*(2*11.73+11.73)/1022) for e in edges])
print(dp2m)
ee = np.array([e[1] for e in edges])
print(p2m)
plot.errorbar(ee, p2m, xerr=11.73, yerr=dp2m, linestyle='none', elinewidth=1, capsize=1, capthick=1)
eel = np.linspace(0, 2000, 100)
plot.plot(eel, eel + eel**2/1022)
plot.plot(eel, eel)
plot.ylabel(r'$p^2/2m$ (keV)')
plot.xlabel(r'$E_e$ (keV)')
plot.legend(['Relativistic', 'Classical'])
plot.title('Classical and Relativistic Predictions for Kinetic Energy')
plot.xlim(0, 2000)
plot.ylim(0, 4e3)
plot.show()

print(ee + ee**2/1022)
print(*[f'{round(e, 2)} & ${round(point, 2)} \\pm {round(dp, 2)}$' for e, point, dp in zip(ee, p2m, dp2m)], sep='\n')
rel = ee + ee**2/1022
cls = ee

print(1 - np.sum((p2m-rel)**2)/np.sum((p2m-np.mean(p2m))**2))
print(1 - np.sum((p2m-cls)**2)/np.sum((p2m-np.mean(p2m))**2))

print(np.std(p2m-rel))
print(np.std(p2m-cls))