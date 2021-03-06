import subprocess
import numpy as np
import matplotlib
import os
import math
import matplotlib.pyplot as plt
from matplotlib import rc

matplotlib.rcParams["mathtext.fontset"] = "stix"
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}',
    r'\usepackage[helvet]{sfmath}', r'\usepackage[utf8]{inputenc}',
    r'\usepackage{arev}', r'\usepackage{siunitx}',
    r'\sisetup{math-micro={\usefont{T1}{phv}{m}{n}\text{µ}}}']

labelFontSize = 16
legendFontSize = 15
lineFontSize = 15

matplotlib.rcParams.update({'font.size': labelFontSize})

fig,ax=plt.subplots()

fractions = [0.0, 0.3, 0.5]
iterations = 1000
D = 10e-12

def get_squared_displacement(track):
  size = len(track)
  sd = np.empty(size)
  x = track[:,0]
  y = track[:,1]
  z = track[:,2]
  for i in range(size):
    sd[i] = math.pow(x[i]-x[0],2) + math.pow(y[i]-y[0],2) + math.pow(
        z[i]-z[0],2)
  return sd

for fraction in fractions: 
  sd = np.array([])
  times = np.array([])
  cnt = 0
  for i in range(iterations): 
    dirname = 'fraction_'+str(fraction)+'__'+str(i)
    print(dirname)
    inputf = dirname+os.sep+'coordinates.spa'
    f = open(inputf, 'r')
    header = f.readline().strip().split(',')
    voxel_radius = float(header[-1].split('=')[1])
    data = np.loadtxt(inputf, delimiter=',', skiprows=1, dtype=np.str)
    tracks = {}
    if (times.size == 0):
      times = data[:,0].astype(float)
    for row in data:
      for species_id, col in enumerate(row[1:]): #skip the first time col
        if col:
          coords = col.split(' ')
          for i in range(0, len(coords), 4):
            x = float(coords[i])
            y = float(coords[i+1])
            z = float(coords[i+2])
            mol_id = int(coords[i+3])
            if mol_id not in tracks:
              tracks[mol_id] = []
            tracks[mol_id].append([x, y, z])

    for mol_id in tracks:
      coords = tracks[mol_id]
      track = np.asarray(coords)
      cnt = cnt + 1
      if (sd.size == 0):
        sd = get_squared_displacement(track)
      else:
        sd = sd + get_squared_displacement(track)
  ax.plot(times/1e-6, sd/cnt/1e-12, 
      label=r'pSpatiocyte ($\phi=%0.1f$, $D=%d$ \si{\micro}m$^{2}$s$^{-1}$)' %(
        fraction, int(D/1e-12)), lw=2)
  np.savetxt('fraction_'+str(fraction)+'.csv', np.transpose([times, sd/cnt]),
      delimiter=',')
  
ax.plot(times/1e-6, 6.0*D*times/1e-12, 'k--', label='6$Dt$')

handles, labels = ax.get_legend_handles_labels()
leg = ax.legend(frameon=False, loc=2, handletextpad=0.3, labelspacing=0.2, handlelength=1.5)
for t in leg.get_texts():
  t.set_fontsize(legendFontSize)   

plt.xticks(size=labelFontSize)
plt.yticks(size=labelFontSize)

ax.tick_params(axis='both', which='major', direction='in', length=8, width=1,
    labelsize=lineFontSize)
ax.tick_params(axis='both', which='minor', direction='in', length=3, width=1,
    labelsize=lineFontSize)
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.set_xlim(0,160)
ax.set_ylim(0,0.012)
ax.set_xlabel('Time, $t$ (\si{\micro}s)', size=labelFontSize)
ax.set_ylabel('Mean-squared displacement (\si{\micro}m$^{2}$)', size=labelFontSize)
fig.tight_layout()
plt.savefig('crowded_diffusion.pdf', format='pdf', dpi=600)
plt.show()





