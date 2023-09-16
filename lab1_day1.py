import numpy as np
import matplotlib.pyplot as plot
from scipy import stats

x = np.array([36+41.5,42+45, 104+103, 172+179, 299+299,
              442+447, 553+543, 612+610, 835+840, 1044+1047, 1247+1275]) # cm
t = np.array([32, 32, 38, 42, 50, 60, 70, 72, 88, 102, 116]) # ns
dx = 2*np.array([0.5, 0.5, 0.5, 0.5, 5, 5, 5, 5, 5, 10, 10])
dt = 2*np.ones(len(t))

reg = stats.linregress(t, x)
print('speed of light = %.5e m/s' % (reg.slope*(10**-2/10**-9)))
print(f'sensor delay = {round(-reg.intercept/reg.slope, 3)} ns')

plot.errorbar(t, x, dx, dt, capsize=3, fmt='none', label='Data', color='#b20')
T = np.linspace(-reg.intercept/reg.slope, t[-1], 100)
plot.plot(T, T*reg.slope+reg.intercept, label='Regression (m=%.2f, b=%.2f)' % (reg.slope, reg.intercept), linestyle='--')

#plot.plot(T, T*299_792_458*10**-7-32*reg.slope, label='Known', color='#00f')

plot.legend()
plot.ylabel('Distance (cm)')
plot.xlabel('Time (ns)')
plot.title('Time for Laser to Reach Detector')
plot.xticks(np.arange(30, 120, 10))

plot.show()
