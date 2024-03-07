import matplotlib.pyplot as plt
import os

from plotting import *


# Load files
grid_files = sorted(os.listdir('./test-run/energies'))

# (3-3)-0 graphs
files_0 = sorted(['./test-run/energies/' + f for f in grid_files if '(3-3)-0' in f])
# reorder the files
files_0 = [files_0[i] for i in (0,1,4,5,3,10,9,6,11,2,8,7)] 
# Plot
draw_multiple_landscapes_and_graphs(files_0, rows=3, cols=4)


# (3-3)-1 graphs
files_1 = ['./test-run/energies/' + f for f in grid_files if '(3-3)-1' in f]
# For reorder purposes add None
files_1.append(None)
# reorder the files
files_1 = [files_1[i] for i in (0,2,3,-1,-1,7,-1,4,9,1,5,6)] 
# Plot
draw_multiple_landscapes_and_graphs(files_1, rows=3, cols=4)

# (3-3)-2 graphs
files_2 = ['./test-run/energies/' + f for f in grid_files if '(3-3)-2' in f]
# reorder the files
files_2 = [files_2 [i] for i in (0,1,4,3,2)] 
# Plot
draw_multiple_landscapes_and_graphs(files_2 , rows=1, cols=5, figsize=(7.166, 7.166/3))

# show
plt.show()