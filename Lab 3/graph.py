from data import *


trials = np.array(list(map(np.array, trials)))

means = np.array([np.mean(arr) for arr in trials])
sigma = np.array([np.std(arr) for arr in trials])

t = np.linspace(theta[0], theta[-1], 100)
t_doubled = np.linspace(360-theta[-1], theta[-1], 100)

normalization = means[1]

linearized = np.sqrt(-np.log(means/normalization))

max_sigma = sigma[means.tolist().index(normalization)]
dlin = -0.5 / linearized / means * (sigma - means/normalization * max_sigma)

print(linearized)
print(means)
print(sigma)
print(dlin)

without = lambda x, i: np.array([*x[:i], *x[i+1:]])

slope = np.sum(linearized)/np.sum(theta-180)
dslope = np.abs(np.sum(without(dlin, 1))/np.sum(without(theta, 1)-180) - np.sum(without(linearized, 1))/np.sum(without(theta, 1)-180)**2 * np.sum(without(dtheta, 1)))

fit_uncertainty_l = np.sqrt(np.mean((linearized-(theta-180)*slope)**2))
fit_uncertainty = np.sqrt(np.mean((means-means[1]*np.exp(-((theta-180)*slope)**2))**2))

plot.plot(theta, means)
plot.plot(theta, means[1]*np.exp(-((theta-180)*slope)**2))

print(slope, dslope, fit_uncertainty_l, fit_uncertainty)
plot.show()

"""
plot.plot(theta, linearized)
plot.fill_between(theta, linearized_up, linearized_down, alpha=0.1)
print(mean_slope)
plot.plot(t, mean_slope*(t-180))
plot.fill_between(t, slope_down*(t-180), slope_up*(t-180), alpha=0.1)
plot.show()
"""

plot.errorbar(np.concatenate([list(reversed(360-theta)), theta]), np.concatenate([list(reversed(means)), means]), yerr=np.concatenate([list(reversed(sigma)), sigma]), xerr=0.5, capsize=2, color='#b20', label='Data', fmt='none')

plot.plot(t_doubled, means[1]*np.exp(-((t_doubled-180)*slope)**2), label='Gaussian Fit', color='green')

plot.fill_between(t_doubled, (means[1]+sigma[1])*np.exp(-((t_doubled-180)*(slope-dslope))**2), (means[1]-sigma[1])*np.exp(-((t_doubled-180)*(slope+dslope))**2), color='#01f', alpha=0.2, linewidth=0)

plot.xlabel(r'$\theta$°')
plot.ylabel('Scintillator Counts')
plot.title('Scintillator Counts by Angle')

plot.legend()
#import scipy.stats
#slope, intercept, r, p, se = scipy.stats.linregress(theta-180, linearized)
#print(slope, intercept/slope)
#plot.plot(t, (t-180)*slope)


plot.show()