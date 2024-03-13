import matplotlib.pyplot as plt
import os

from plotting import *


# Use Latex font
plt.rcParams.update({
    "font.family": "Helvetica"
})

# Load files
grid_files = sorted(os.listdir('./energies/ordered'))
files = [None]*3
figsize = (7.166, 7.166)

ordering = [(0,1,7,6,2,3,9,8,4,5,11,10),
            (0,2,3,-1,-1,7,-1,4,9,1,5,6),
            (0,1,4,3,2)]

for k in range(1):
    # (3-3)-k graphs
    name_list = sorted(['./energies/ordered/' + name for name in grid_files if f'(3-3)-{k}' in name])
    files[k]= name_list
    # For reorder purposes add None
    name_list.append(None)
    # reorder the files
    files[k] = [name_list[i] for i in ordering[k]]
    # Plot
    draw_multiple_landscapes_and_graphs(files[k], rows=3, cols=4, figsize=figsize)
    # plt.savefig(f'(3-3)-{k}.pdf')

# Plot
# draw_multiple_landscapes_and_graphs(files[2] , rows=1, cols=5, figsize=(7.166, 7.166/3))
plt.savefig('(3-3)-0-landscapes.pdf')

# show
# plt.show()