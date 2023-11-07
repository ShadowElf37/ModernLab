import numpy as np
import matplotlib.pyplot as plot

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
  'co57': (141, 666),
  'ba133': (356,),
  'cs137': (675,),
  'cd109': (675,),
}

for file in files:
    data = np.load(file)
    fname = os.path.splitext(file)[0]
    element = fname[:2].capitalize() + '-' + fname[2:]

    plot.figure(figsize=[7.2, 4.8])

    for E in photopeaks[fname]:
        plot.axvline(x=E, color='red', linewidth=0.5)
    plot.scatter(data[1], data[0], s=2)
    print((data[1][1]-data[1][0]))
    #plot.scatter(data[1], -np.sqrt(data[0])*np.gradient(np.gradient(data[0]))/(data[1][1]-data[1][0]), s=1)
    print(list(data[1]))
    MIN = None
    MAX = None
    for p in real_photopeaks[fname]:
        peaki = np.argmin(abs(data[1]-p))
        for i, _ in enumerate(reversed(data[0][:peaki+1])):
            if fname == 'na22': print(data[0][:peaki+1])
            if data[0][peaki-i] > data[0][peaki-i+1]:
                MIN = data[1][peaki-i+1]
            if MIN and data[0][peaki-i] < data[0][peaki-i+1]:
                MAX = data[1][peaki-i+1]
                break
        print(MIN, MAX)
        plot.axvline(x=MIN/2+MAX/2, color='green', linewidth=0.5)

    plot.ylabel('Counts')
    plot.xlabel('Energy (keV)')
    #plot.xticks(data[1][data[1]<1500])
    plot.xlim([0, 1500])
    plot.title('Number of Events by Energy (%s)' % element)
    #plot.savefig('images/%s.png' % fname)

plot.show()