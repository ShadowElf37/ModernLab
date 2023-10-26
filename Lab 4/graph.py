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
  'cs127': (661,),
  'cd109': (),
}

for file in files:
    data = np.load(file)
    fname = os.path.splitext(file)[0]
    element = fname[:2].capitalize() + '-' + fname[2:]

    plot.figure(figsize=[7.2, 4.8])

    for E in photopeaks[fname]:
        plot.axvline(x=E, color='red', linewidth=0.5)
    plot.scatter(data[1], data[0], s=2)

    plot.xlim([0, 1500])
    plot.ylabel('Counts')
    plot.xlabel('Energy (keV)')
    plot.title('Number of Events by Energy (%s)' % element)
    plot.savefig('images/%s.png' % fname)