import os

import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt


from circuit_generation import *
from calculations import *
from plotting import *
from graph_management import *




energy_grids = sorted(os.listdir('./energies/ordered'))

n = len(energy_grids)
transfer_map = np.empty((n, n))
diff_map = np.empty((n, n))

# for i in range(n):
#   acceptor = np.load(f'./energies/ordered/{energy_grids[i]}')
#   for j in range(n):
#     donor = np.load(f'./energies/ordered/{energy_grids[j]}')
#     transfer_map[i,j] = transferability_coeff(donor, acceptor)
#     diff_map[i,j] = average_difference(donor, acceptor)

# np.save('./test-run/transferability-map.npy', transfer_map)
# np.save('./test-run/diff-map.npy', diff_map)
# exit()

transfer_map = np.load('./test-run/transferability-map.npy')
diff_map = np.load('./test-run/diff-map.npy')

# plotting
cm = 1 / 2.54
#fig, ax = plt.subplots(figsize=(38.0*cm, 30.4*cm))
fig, ax = plt.subplots(figsize=(7.166, 7.166))
ax.set_xlabel('Donor subgraph', fontsize='x-large')
ax.set_ylabel('Acceptor subgraph', fontsize='x-large')
img = ax.imshow(transfer_map, cmap='inferno', interpolation='nearest')  # transferability
# img = ax.imshow(diff_map, cmap='inferno_r', interpolation='nearest')  # avg-diff
plt.colorbar(img)

# line seperators
location = -0.5  # seperator between pixels
ticks = []
labels = []
# for x in [3, 4, 5]:
#   for i in range(x):
#     numbers = eval(f'ws_numbers_{x}reg{i}')
#     location += len(numbers)
#     if location < len(energy_grids) - 1:  # skip last lines
#       ax.axvline(x=location, color='white', linestyle='--')
#       ax.axhline(y=location, color='white', linestyle='--')

#     ticks.append(location - len(numbers)/2)
#     labels.append(f'{x}reg{i}')
    
# plt.xticks(ticks, labels)
# plt.yticks(ticks, labels)
ax.xaxis.tick_top()
plt.title('Transferability coefficients', fontsize='30', y=1.05)
plt.show()
#plt.savefig('transferability_map.pdf')
#fig.tight_layout()
#plt.savefig('difference_map.svg', bbox_inches='tight', format='svg', dpi=400)
