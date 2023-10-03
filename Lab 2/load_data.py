import numpy as np
import matplotlib.pyplot as plot
from decimal import Decimal

with open('rtky_no_N2') as f:
    data = f.readlines()
    data = map(lambda s: tuple(map(Decimal, s.strip().split('\t'))), data)
    V, plate, shield = map(np.array,zip(*list(data)))

with open('rtky_N2') as f:
    data = f.readlines()
    data = map(lambda s: tuple(map(Decimal, s.strip().split('\t'))), data)
    V_n2, plate_n2, shield_n2 = map(np.array,zip(*list(data)))

plate_error = [Decimal('0.5e%d' % dec.as_tuple().exponent) for dec in plate]
shield_error = [Decimal('0.5e%d' % dec.as_tuple().exponent) for dec in shield]
plate_n2_error = [Decimal('0.5e%d' % dec.as_tuple().exponent) for dec in plate_n2]
shield_n2_error = [Decimal('0.5e%d' % dec.as_tuple().exponent) for dec in shield_n2]


fig, (ax1, ax2) = plot.subplots(1,2)
ax1.plot(V, np.array(list(map(float,plate_error))))
ax1.set_xlabel('Accelerating Voltage (V)')
ax1.set_ylabel('Current Error (A)')
ax1.set_title('Plate Current Error')
ax2.plot(V, np.array(list(map(float,shield_error))))
ax2.set_xlabel('Accelerating Voltage (V)')
ax2.set_ylabel('Current Error (A)')
ax2.set_title('Shield Current Error')

fig.suptitle('Plate and Shield Current Errors (same for N2/No N2)')


Ps_error = np.abs(plate_error*shield_n2/(shield*plate_n2) + plate*(shield_n2_error/(shield*plate_n2) + shield_n2*(shield**-2*plate_n2**-1*shield_error + shield**-1*plate_n2**-2*plate_n2_error)))
Ps = 1-plate*shield_n2/(shield*plate_n2)
sigma_error = abs(1/(1-Ps)/Decimal(0.7) * Ps_error)

fig, axis = plot.subplots(1,1)
axis.plot(V, plate_n2/shield_n2)
axis.set_xlabel('Accelerating Voltage (V)')
axis.set_ylabel('$f(V)$')
axis.set_title('Geometrical Factor $f(V)$')

fig, (axis, axis2) = plot.subplots(1,2)
axis.plot(np.sqrt(V), np.array(list(map(float, Ps_error))))
#axis.set_ylim([0, 1])
axis.set_ylabel('Probability of Scattering Error $dP_s$')
axis.set_xlabel('Electron Momentum ($\sqrt{V}$)')
axis.set_xlim([0.5, np.sqrt(5)])

sigma = -np.log(1-np.array(list(map(float, Ps))))/0.7
Ps_array = np.array(list(map(float, Ps)))
axis2.plot(np.sqrt(V), np.array(list(map(float, sigma_error))))
axis2.set_ylabel('Scattering Cross-Section Error $d(n\sigma)$ $(\mathrm{cm}^{-1})$')
axis2.set_xlabel('Electron Momentum ($\sqrt{V}$)')
axis2.set_xlim([0.5, np.sqrt(5)])
#axis2.set_ylim([0, 5])

fig.suptitle('Scattering Probability and Cross-Section Error')

#axis.fill_between(np.sqrt(V), Ps+Ps_error, Ps-Ps_error, alpha=0.1)
plate = plate*10**6
shield = shield * 10**3
plate_n2 = plate_n2 * 10**6
shield_n2 = shield_n2*10**3

fig, axes = plot.subplots(2,2)

fig.suptitle('Current Data')

axes[0,0].plot(V, -plate, label='No N2')
axes[0,0].set_title('No N2')
axes[0,0].set_ylabel('Plate Current (µA)')

axes[1,0].plot(V, -shield)
axes[1,0].set_xlabel('Accelerating Voltage (V)')
axes[1,0].set_ylabel('Shield Current (mA)')

axes[0,1].plot(V_n2, -plate_n2, label='N2', color='#f90')
axes[0,1].set_title('N2')

axes[1,1].plot(V_n2, -shield_n2, label='N2', color='#f90')
axes[1,1].set_xlabel('Accelerating Voltage (V)')



plot.show()


s = sigma
s[s is float('NaN') or V < 0.3] = 100
s = list(s)

plot.plot(V[V > 0.3], sigma[V > 0.3])

print(s)
print(min(s))
print(sigma_error[s.index(min(s))])
print(V[s.index(min(s))])
plot.show()

