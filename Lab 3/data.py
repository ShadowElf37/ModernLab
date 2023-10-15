import numpy as np
import matplotlib.pyplot as plot

theta = np.array([180, 182, 185, 187, 190, 192, 195, 197, 200, 202, 205, 210, 215])
dtheta = 0.5*np.ones_like(theta)

trials = [
    [322, 209, 284, 308, 298, 303, 323, 323, 299, 291], #180
    [290, 295, 328, 285, 330, 282, 309, 315, 285, 295], # 182
    [272, 287, 289, 296, 282, 264, 266, 271, 281, 292], # 185
    [250, 259, 267, 242, 254, 247, 261, 230, 254, 252], # 187
    [234, 181, 222, 197, 193, 187, 196, 189, 192, 206], # 190
    [174, 177, 168, 180, 134, 163, 164, 176, 176, 170], # 192
    [137, 96,  121, 138, 101, 97,  112, 106, 122, 114], # 195
    [73,  61,  75,  85,  75,  74,  79,  71,  87,  75 ], # 197
    [45,  41,  39,  51,  55,  46,  52,  42,  39,  36 ], # 200
    [32,  25,  29,  27,  26,  34,  31,  27,  27,  38 ], # 202
    [7, 5, 13, 8, 10, 3, 3, 3, 4, 7], # 205
    [1, 2, 5, 1, 1, 3, 2, 5, 1, 1], # 210
    [1, 3, 3, 1, 1, 2, 2, 1, 2, 4], # 215
]


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

print(slope, dslope)

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