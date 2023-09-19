import numpy as np
import matplotlib.pyplot as plot
from scipy import stats

N = 10
x = np.array([6,7,8,9,10,11,12,13,14,15])
x = (np.sqrt(x**2+1)+x)*12*2.54# cm
t = np.array([36,37,40,41,44,46,47,49,52,53])#+np.array([1,1,1,1,1,-1,-1,-1,-1,-1])*1 # ns
dx = np.ones(N)*2.54
dx = dx + dx*(x/np.sqrt(x**2+(12*2.54)**2))
#print(dx)
dt = np.ones(N)

def regression(dt_input=0, dx_input=0):
    modified_t = t + dt_input
    modified_x = x + dx_input

    A = np.column_stack((np.ones(N), modified_t))
    return np.linalg.inv(A.T @ A) @ A.T @ modified_x

XLIM = [35, 54]
T = np.linspace(*XLIM, 100)

mean_reg = regression()
x0, c = mean_reg
errors_t = []
errors_x = []
for i in range(N):
    dt_input = np.zeros(N)
    dt_input[i] = dt[i]
    #errors_t.append(np.max(np.array([np.abs(regression(dt_input) - mean_reg), np.abs(regression(-dt_input) - mean_reg)]), 0))
    errors_t.append(np.array(regression(dt_input) - mean_reg))
    dx_input = np.zeros(N)
    dx_input[i] = dx[i]
    #errors_x.append(np.max(np.array([np.abs(regression(0,dx_input) - mean_reg), np.abs(regression(0,-dx_input) - mean_reg)]), 0))
    errors_x.append(np.array(regression(0,dx_input) - mean_reg))

#plot.plot(T, T * (c + errors_x[-1][1]) + x0 + errors_x[-1][0], alpha=0.1, color='#f00')

errors_t = np.array(errors_t)
errors_x = np.array(errors_x)

print(errors_t[:,0])

cov_00 = np.sum(errors_t[:,0]**2+errors_x[:,0]**2)
cov_cc = np.sum(errors_t[:,1]**2+errors_x[:,1]**2)
cov_c0 = np.sum(errors_t[:,0]*errors_t[:,1]+errors_x[:,0]*errors_x[:,1])

cov = np.array([[cov_cc, cov_c0], [cov_c0, cov_00]])/N
dc = np.sqrt(cov[0,0])
dx0 = np.sqrt(cov[1,1])
dcx2 = cov[1,0]
t0 = -x0/c

print(cov)
#x = ct-x0
#var(x) = np.sqrt(t**2*cov[0,0]-cov[1,1] + 2*t*cov[1,0])



plot.errorbar(t, x, dx, dt, capsize=3, fmt='none', label='Data', color='#b20')
plot.plot(T, T * c + x0, label='Regression (m=%.2f±%.2f, b=%.2f±%.2f)' % (c, dc, x0, dx0), linestyle='--')

#xstd_plus = np.sqrt(T**2*cov[0,0]+cov[1,1] + 2*T*cov[1,0])
#xstd_minus = np.sqrt(T**2*cov[0,0]+cov[1,1] - 2*T*cov[1,0])

plot.fill_between(T, T*(c+dc)+x0+dx0, T*(c-dc)+x0-dx0, alpha=0.15,linewidth=0)

sxm = (T**2*dc**2 + dx0**2 - 2*T*cov[1,0])
sxm = np.sqrt(np.abs(sxm))*np.sign(sxm)
#plot.fill_between(T, T*c+x0 - sxm, T*c+x0 + sxm, alpha=0.15,linewidth=0, color='#f70')


plot.legend(loc='upper left')
plot.ylabel('Distance (cm)')
plot.xlabel('Time (ns)')
plot.title('Time for Laser to Reach Detector')
plot.xticks(np.arange(*XLIM, 3))

t0 = -x0/c
dt0 = dx0/c - x0/c**2 * dc
print(f'Speed of light: {c/10} ± {dc/10} 10^8 m/s\nSensor delay: {t0} ± {dt0} ns')

plot.show()