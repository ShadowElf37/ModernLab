import numpy as np
import matplotlib.pyplot as plot
from scipy import stats

x = np.array([6,7,8,9,10,11,12,13,14,15])
x = (np.sqrt(x**2+1)+x)*12*2.54 # cm
t = np.array([36,37,40,41,44,46,47,49,52,53]) # ns
dx = np.ones(len(t))*2.54
dx = dx + dx*(x/np.sqrt(x**2+(12*2.54)**2))
dt = np.ones(len(t))


#meanx = (x[-1] + x[0]) / 2
#meant = (t[-1] + t[0]) / 2
meanx = np.mean(x)
meant = np.mean(t)
print(meanx, meant)
x = x - meanx
t = t - meant

slope = np.mean(x/t)
ds = np.mean((dx/t - x/t**2 * dt))

c = slope*(10**-2/10**-9)
dc = ds * (10**-2/10**-9)

print('speed of light = %.3fe8 ± %.3fe8 m/s' % (c/10**8, dc/10**8))

plot.errorbar(t, x, dx, dt, capsize=3, fmt='none', label='Data', color='#b20')
plot.scatter(meant, meanx)
#T = np.linspace(35, 54, 100)
T = np.linspace(-10, 10, 100)
plot.plot(T, T*slope)
plot.show()


print('speed of light = %.5e m/s' % (reg.slope*(10**-2/10**-9)))
print(f'sensor delay = {round(delay, 3)} ns')

plot.errorbar(t, x, dx, dt, capsize=3, fmt='none', label='Data', color='#b20')
time_intercept = -reg.intercept/reg.slope
T = np.linspace(35, 54, 100)
plot.plot(T, T*reg.slope+reg.intercept, label='Regression (m=%.2f±%.2f, b=%.2f±%.2f)' % (reg.slope, c_s, reg.intercept, delay_s), linestyle='--')



plot.fill_between(T, T*(reg.slope-c_s)+reg.intercept-delay_s, T*(reg.slope+c_s)+reg.intercept+delay_s, alpha=0.2)
#plot.plot(T, T*(reg.slope+sdev)+reg.intercept+isdev, label='Regression (m=%.2f, b=%.2f)' % (reg.slope, reg.intercept), linestyle='--')
#plot.plot(T, T*(reg.slope-sdev)+reg.intercept-isdev, label='Regression (m=%.2f, b=%.2f)' % (reg.slope, reg.intercept), linestyle='--')


#plot.plot(T, T*299_792_458*10**-7-32*reg.slope, label='Known', color='#00f')

plot.legend()
plot.ylabel('Distance (cm)')
plot.xlabel('Time (ns)')
plot.title('Time for Laser to Reach Detector')
plot.xticks(np.arange(35, 54, 3))

plot.show()
