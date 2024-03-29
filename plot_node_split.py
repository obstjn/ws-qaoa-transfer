import matplotlib.pyplot as plt
import os

from plotting import *


# Use Latex font
plt.rcParams.update({
    "font.family": "Helvetica"
})

# Load files
grid_files = sorted(os.listdir('./test-run/energies'))

# (3-3)-0 graphs
files_0 = sorted(['./test-run/energies/' + f for f in grid_files if '(3-3)-0' in f])
# reorder the files
files_0 = [files_0[i] for i in (0,1,4,5,3,10,9,6,11,2,8,7)] 
# (3-3)-1 graphs
files_1 = ['./test-run/energies/' + f for f in grid_files if '(3-3)-1' in f]
# For reorder purposes add None
files_1.append(None)
# reorder the files
files_1 = [files_1[i] for i in (0,2,3,-1,-1,7,-1,4,9,1,5,6)] 
# (3-3)-2 graphs
files_2 = ['./test-run/energies/' + f for f in grid_files if '(3-3)-2' in f]
# reorder the files
files_2 = [files_2 [i] for i in (0,1,4,3,2)] 

files_1 = ['./test-run/energies/' + f for f in grid_files if '(3-3)-1' in f]
node_split_files = [files_0[9], files_1[1], files_1[8], files_2[1]]

# Plot
draw_multiple_landscapes_and_graphs(node_split_files , rows=1, cols=4, figsize=(7.166, 7.166/3))

# show
plt.show()
# plt.savefig('node_split.pdf')