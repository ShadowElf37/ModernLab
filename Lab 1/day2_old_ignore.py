import numpy as np
import matplotlib.pyplot as plot
from scipy import stats

x = np.array([6,7,8,9,10,11,12,13,14,15])
x = (np.sqrt(x**2+1)+x)*12*2.54# cm
t = np.array([36,37,40,41,44,46,47,49,52,53])#+np.array([1,1,1,1,1,-1,-1,-1,-1,-1])*1 # ns
dx = np.ones(len(t))*2.54
dx = dx + dx*(x/np.sqrt(x**2+(12*2.54)**2))
#print(dx)
dt = np.ones(len(t))

print(*list(map(lambda g: list(map(lambda n: np.round(n, 3),g)), (x, t, dx, dt))), sep='\n')

reg = stats.linregress(t, x)
slope = reg.slope
intercept = reg.intercept

c = (slope*(10**-2/10**-9))
delay = -intercept/slope

dslope = np.sqrt(np.mean((dx / t) ** 2 + ((x - reg.intercept) / t ** 2 * dt) ** 2))
dintercept = np.sqrt(np.mean(dx ** 2 + (slope * dt) ** 2))

dc = dslope * (10 ** -2 / 10 ** -9)
ddelay = dintercept / slope

print('speed of light = %.5fe8 m/s ± %.5fe8' % (c / 10 ** 8, dc / 10 ** 8))
print(f'sensor delay = {round(delay, 3)} ± {round(ddelay, 3)} ns')

res = x - intercept - slope*t
print(res)
sx = np.std(res)
print(sx**2/t)

plot.errorbar(t, x, dx, dt, capsize=3, fmt='none', label='Data', color='#b20')
time_intercept = -reg.intercept/reg.slope
T = np.linspace(35, 54, 100)
plot.plot(T, T * reg.slope + reg.intercept, label='Regression (m=%.2f±%.2f, b=%.2f±%.2f)' % (reg.slope, dslope, reg.intercept, dintercept), linestyle='--')

plot.fill_between(T, T * (reg.slope - dslope) + reg.intercept - dintercept, T * (reg.slope + dslope) + reg.intercept + dintercept, alpha=0.2)

plot.legend(loc='upper left')
plot.ylabel('Distance (cm)')
plot.xlabel('Time (ns)')
plot.title('Time for Laser to Reach Detector')
plot.xticks(np.arange(35, 54, 3))

plot.show()
