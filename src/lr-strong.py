#!/usr/bin/python
import os
import sys
import numpy as np
import matplotlib.cm as cmx
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from matplotlib import rc

# Configure matplot to understand tex grammer.
# rc('text', usetex=True)
rc('font', size=24)

fig = plt.figure(figsize=(10.5, 5))
ax  = fig.add_axes( [.10, .25, .85, .49 ]) 

N = 3
P = 5

width = 0.2
sep  = .05
add_text = False
ylim = 3.99

Legends = [
'Runtime Overhead',
'Task Execution Time'
]

busy_times = [    
  ["Nimbus"         ,  0.195, 0.078, 0.041],
  ["Spark"          , 11.511, 4.335, 2.068],
  ["Naiad"          ,  1.900, 0.760, 0.380],
  ["Spark-opt"      ,  0.283, 0.111, 0.054],
  ["Naiad-opt"      ,  0.200, 0.080, 0.041]
#  ["Nimbus-no-temp" ,  0.195, 0.078, 0.041],
]

idle_times = [    
  ["Nimbus"         , 0.019, 0.018, 0.025],
  ["Spark"          , 1.046, 0.958, 0.791],
  ["Naiad"          , 0.080, 0.280, 0.904],
  ["Spark-opt"      , 0.249, 0.468, 0.944],
  ["Naiad-opt"      , 0.083, 0.272, 0.904]
#  ["Nimbus-no-temp" , 0.098, 0.403, 0.982],
]


n_colors = P
color_map = cmx.ScalarMappable(
        colors.Normalize(vmin=0, vmax=n_colors+1), cmap='Greys')
Colors = [color_map.to_rgba(i) for i in range(n_colors, -1, -1)]


def plot_bar(bar_data, ind, bottom, color, t_color, hatch, add_sum):
    p = ax.bar(ind, bar_data, width, color=color, hatch=hatch, bottom=bottom)

    idx = 0
    for num, rect in zip(bar_data, p):
      if (add_text):
        plt.text(rect.get_x() + rect.get_width()/2.,
                 rect.get_y()+ rect.get_height()/2.,
                 '{:.2f}'.format(num),
                 ha='center', va='center',
                 color=t_color,
                 fontsize='small')
      if add_sum and num+bottom[idx] < ylim:
        offset = .8
        if num+bottom[idx] < .4:
          format='{:.3f}'
        else:
          format='{:.2f}'
          offset -= .1
        plt.text(rect.get_x() + rect.get_width()/2,
                 rect.get_y()+ rect.get_height() + offset,
                 format.format(num+bottom[idx]),
                 ha='center', va='center',
                 rotation='90',
                 fontsize='medium')

      idx += 1

    for i in range(0, len(bottom)):
        bottom[i] += bar_data[i]
    return p


Parts = []

for i in range(0, P): 
  bottom = [0] * N
  ind = (np.arange(N)) * (width + sep) + i
  pc = plot_bar(busy_times[i][1:], ind, bottom, '#5CB85C', 'w', '', False)
  pi = plot_bar(idle_times[i][1:], ind, bottom, 'w', 'k', '', True)

Parts.append(pi)
Parts.append(pc)


xlabels = []
xticks  = []
for i in range(0, P):
  xlabels.extend(['20', '50', '100'])
  ind = (np.arange(N)) * (width + sep) + i + width/2
  xticks.extend(ind)

xticks.extend((np.arange(P) + 1.5 * (width + sep)))
for i in range(0, P):
  xlabels.extend([busy_times[i][0]])

ax.set_xticks(xticks)
ax.set_xticklabels(xlabels)

idx = 1
for t in ax.get_xticklabels():
  if (idx > P * N):
    t.set_y(-.15)
    t.set_fontsize("small")
    t.set_fontweight("normal")
  else:
    # t.set_rotation(30)
    t.set_fontsize("x-small")
    t.set_fontweight("normal")
  idx += 1

al = .6

ax.annotate("12.56", xy=(1 + width/2, ylim),
            xytext=(1 + width/2,ylim + al),
            size="medium",
            va="bottom", ha="center",
            rotation='90',
            arrowprops=dict(arrowstyle="<|-", fc='k', lw=2))

ax.annotate("5.30", xy=(1 + (width + sep) + width/2, ylim),
            xytext=(1 + (width + sep) + width/2,ylim + al),
            size="medium",
            va="bottom", ha="center",
            rotation='90',
            arrowprops=dict(arrowstyle="<|-", fc='k', lw=2))


ax.set_xlim(-width/2, P - width)

ax.spines['top'].set_visible(False)
ax.tick_params(axis='x', which='both', top='off')

ax.set_ylim([0, ylim])
ax.set_yticks(np.linspace(0,3,4))



plt.legend(Parts, Legends,
           ncol=1, loc='upper right', # mode='expand'
           bbox_to_anchor=(1, 1.5),
           fontsize='medium', frameon=False)


ax.set_xlabel('Number of Workers', fontsize='medium', fontweight='normal', labelpad=8)
ax.set_ylabel('Iteration time (s)', fontsize='medium', fontweight='normal', labelpad=10)


plt.savefig(os.path.dirname(os.path.realpath(__file__)) + '/../images/lr-strong.png')

if len(sys.argv) >= 2:
  if sys.argv[1] == '-s':
    plt.show()


