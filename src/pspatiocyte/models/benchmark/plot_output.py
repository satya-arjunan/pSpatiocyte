import os
import sys
import numpy
import csv
import math
from matplotlib import rc
from pylab import *
from collections import OrderedDict

matplotlib.rcParams["mathtext.fontset"] = "stix"
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}',
    r'\usepackage[helvet]{sfmath}', r'\usepackage[utf8]{inputenc}',
    r'\usepackage{arev}', r'\usepackage{siunitx}',
    r'\sisetup{math-micro={\usefont{T1}{phv}{m}{n}\text{µ}}}']

labelFontSize = 16
legendFontSize = 14
lineFontSize = 15

path, file = os.path.split(os.path.abspath(__file__))
path = path+os.sep

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
    (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
    (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
    (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
    (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)  

colors = [0, 8, 4, 2, 3]

linestyles = OrderedDict(
    [('solid',               (0, ())),
     ('loosely dotted',      (0, (1, 10))),
     ('dotted',              (0, (1, 5))),
     ('densely dotted',      (0, (1, 1))),

     ('loosely dashed',      (0, (5, 10))),
     ('dashed',              (0, (5, 5))),
     ('densely dashed',      (0, (5, 1))),

     ('loosely dashdotted',  (0, (3, 10, 1, 10))),
     ('dashdotted',          (0, (3, 5, 1, 5))),
     ('densely dashdotted',  (0, (3, 1, 1, 1))),

     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))])

fileNames = ['pspatiocyte/output.txt', 'spatiocyte/output.txt', 'smoldyn/output.txt', 'readdy/output.txt', 'readdy_serial/output.txt']
legendTitles = ['pSpatiocyte (8 cores, $\Delta t=0.5\ \mathrm{ms},\ T=10\ \mathrm{s}$)','Spatiocyte ($\Delta t=0.5\ \mathrm{ms}, T=139\ \mathrm{s}$)','Smoldyn ($\Delta t=1\ \mathrm{ms},\ T=449\ \mathrm{s}$)','Parallel ReaDDy (8 cores, $\Delta t=1\ \mathrm{ms}, T=549\ \mathrm{s}$)','Serial ReaDDy ($\Delta t=1\ \mathrm{ms}, T=2197\ \mathrm{s}$)']
speciesList = ['E','S','ES','P']
lines = ['-','-','-','-','-','-','-']
opacity = [1, 1, 1, 1, 1]

volume = 909.
for f in reversed(range(len(fileNames))):
  if (os.path.isfile(path+fileNames[f])):
    deli = ','
    if (f == 2):
      deli = ' '
    data = genfromtxt(path+fileNames[f], delimiter=deli, skip_header=1).T
    colSize = len(data)-1
    for i in range(colSize):
      if (i == 0):
        plot(data[0], data[i+1]/volume, ls=lines[f], 
            color=tableau20[colors[f]], label=legendTitles[f],
            linewidth=2.5, alpha=opacity[f])
      else:
        plot(data[0], data[i+1]/volume, ls=lines[f],
            color=tableau20[colors[f]], linewidth=2.5, alpha=opacity[f])

n_particles_e = 9090
n_particles_s = 90910
duration = 100.0

from scipy.integrate import odeint

def f(x, t0, kf, kr, kcat):
    """
    x: state vector with concentrations of E, S, ES, P
    """
    return np.array([
        -kf * x[0] * x[1] + (kr+kcat)*x[2],
        -kf * x[0] * x[1] + kr * x[2],
        kf * x[0] * x[1]- (kr+kcat)*x[2],
        kcat*x[2]
    ])

init_state = np.array([n_particles_e, n_particles_s, 0., 0.]) / volume
ode_time = np.linspace(0.,duration,100000)
ode_result = odeint(f, y0=init_state, t=ode_time, args=(0.98e-2, 1., 1.))

plot(ode_time, ode_result[:,0], "--", color="k", label="ODE")
plot(ode_time, ode_result[:,1], "--", color="k")
plot(ode_time, ode_result[:,2], "--", color="k")
plot(ode_time, ode_result[:,3], "--", color="k")


annotate('ES', xy=(9, 0),  xycoords='data', xytext=(-29, -10), textcoords='offset points', color='k', size=lineFontSize)

annotate('E', xy=(9, 5),  xycoords='data', xytext=(-27, 15), textcoords='offset points', color='k', size=lineFontSize)

annotate('P', xy=(9, 23),  xycoords='data', xytext=(-27, 12), textcoords='offset points', color='k', size=lineFontSize)

annotate('S', xy=(9, 64),  xycoords='data', xytext=(-27, 32), textcoords='offset points', color='k', size=lineFontSize)


annotate(r'E + S $\overset{k_1}{\underset{k_2}\rightleftharpoons}$ ES $\overset{k_3}{\rightarrow}$ E + P', xy=(6, 85),  xycoords='data', xytext=(-29, 0), textcoords='offset points', color='k', size=lineFontSize)

ax = gca()
handles, labels = ax.get_legend_handles_labels()
leg = legend(handles[::-1], labels[::-1], loc=(0.02,0.34), labelspacing=0.3, handlelength=1.5, handletextpad=0.8, frameon=False)
for t in leg.get_texts():
  t.set_fontsize(legendFontSize)   

xticks(size=labelFontSize)
yticks(size=labelFontSize)

ax.tick_params(axis='both', which='major', direction='in', length=8, width=1,
    labelsize=lineFontSize)
ax.tick_params(axis='both', which='minor', direction='in', length=3, width=1,
    labelsize=lineFontSize)
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
xlabel('Time, $t$ (s)',size=labelFontSize)
ylabel("Concentration (\#\si{\micro}m$^{-3}$)",size=labelFontSize)
xlim(0,10)
tight_layout()
savefig('benchmark_output.pdf', format='pdf', dpi=600)#, bbox_inches='tight')
show()


