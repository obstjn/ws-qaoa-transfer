import matplotlib.pyplot as plt
import os

from plotting import *


# Load files
grid_files = sorted(os.listdir('./test-run/energies'))
files = [None]*5
figsize = (7.166, 7.166)

ordering = [(0,1,3,10,12,14,6,8,24,23,15,9,25,27,29,16,18,21,2,4,7,17,11,13,26,28,5,20,19,22),
            (0,2,6,12,15,-1,9,-1,26,-1,-1,10,28,32,35,18,22,25,1,4,8,17,11,14,27,30,5,21,20,24),
            (0,3,8,13,-1,-1,-1,-1,25,-1,-1,10,28,32,-1,18,23,-1,1,5,9,16,11,14,26,7,2,17,22,24),
            (0,4,-1,-1,-1,-1,-1,-1,14,-1,-1,6,18,-1,-1,12,-1,-1,1,5,-1,9,7,-1,3,19,2,10,13,-1),
            (0,1,2,7,6,3,4,5)]

for k in range(5):
    # (5-5)-k graphs
    name_list = sorted(['./test-run/energies/' + name for name in grid_files if f'(5-5)-{k}' in name])
    files[k]= name_list
    # For reorder purposes add None
    name_list.append(None)
    # reorder the files
    files[k] = [name_list[i] for i in ordering[k]]
    # Plot
    draw_multiple_landscapes_and_graphs(files[k], rows=5, cols=6, figsize=figsize)
    plt.savefig(f'(5-5)-{k}.pdf')

# Plot
draw_multiple_landscapes_and_graphs(files[4], rows=2, cols=4, figsize=figsize)
plt.savefig('(5-5)-4.pdf')

# show
# plt.show()