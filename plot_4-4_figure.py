import matplotlib.pyplot as plt
import os

from plotting import *


# Load files
grid_files = sorted(os.listdir('./test-run/energies'))
files = [None]*4
figsize = (7.166, 7.166)

ordering = [(0,1,3,5,16,17,19,2,4,18,13,11,8,12,14,9,7,6,10,15),
            (0,2,5,-1,15,17,20,1,4,16,14,11,7,10,13,-1,8,6,9,-1),
            (0,3,-1,-1,12,15,-1,1,4,2,-1,10,6,8,11,-1,-1,5,7),
            (0,1,5,4,2,3)]

for k in range(4):
    # (4-4)-k graphs
    name_list = sorted(['./test-run/energies/' + name for name in grid_files if f'(4-4)-{k}' in name])
    files[k]= name_list
    # For reorder purposes add None
    name_list.append(None)
    # reorder the files
    files[k] = [name_list[i] for i in ordering[k]]
    # Plot
    draw_multiple_landscapes_and_graphs(files[k], rows=4, cols=5, figsize=figsize)
    # plt.savefig(f'(4-4)-{k}.pdf')

# Plot
draw_multiple_landscapes_and_graphs(files[3], rows=2, cols=3, figsize=figsize)
# plt.savefig('(4-4)-3.pdf')

# show
plt.show()
