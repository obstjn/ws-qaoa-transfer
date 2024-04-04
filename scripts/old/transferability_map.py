import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt


from circuit_generation import *
from calculations import *
from plotting import *
from graph_management import *


ws_numbers_3reg0 = [0, 2, 8, 72, 74, 164, 62, 56, 18, 26, 20, 182]
ws_numbers_3reg1 = [0, 2, 60, 20, 78, 56, 6, 8, 24]
ws_numbers_3reg2 = [0, 6, 24, 8, 2]

ws_numbers_4reg0 = [0, 1, 3, 7, 24, 25, 27, 33, 35, 57, 23, 19, 17, 8, 15, 11, 9, 51, 41, 43]
ws_numbers_4reg1 = [0, 1, 3, 20, 21, 11, 8, 9, 28, 19, 17, 4, 7, 5, 25, 12, 13]
ws_numbers_4reg2 = [0, 1, 18, 13, 4, 5, 22, 17, 2, 3, 21, 6, 7]
ws_numbers_4reg3 = [0, 2, 6, 14, 1, 3]

ws_numbers_5reg0 = [0, 1, 3, 7, 15, 48, 49, 51, 55, 65, 67, 71, 113, 115, 195, 47, 39, 35, 33, 16, 31, 23, 19, 17, 103, 99, 81, 87, 83, 211]
ws_numbers_5reg1 = [0, 1, 3, 7, 40, 41, 43, 23, 16, 17, 19, 56, 57, 81, 39, 35, 33, 15, 11, 9, 51, 49, 24, 27, 25, 89]
ws_numbers_5reg2 = [0, 1, 3, 36, 37, 27, 8, 9, 11, 44, 45, 60, 35, 33, 7, 5, 43, 41, 12, 15, 13, 28]
ws_numbers_5reg3 = [0, 1, 34, 29, 4, 5, 28, 13, 12, 33, 3, 37, 6, 7, 14]
ws_numbers_5reg4 = [0, 2, 6, 14, 30, 1, 3, 7]


energy_grids = []
for x in [3, 4, 5]:
  for i in range(x):
    numbers = eval(f'ws_numbers_{x}reg{i}')
    for k in numbers:
      grid = np.load(f'./ws-energies/{x}reg{i}/energies/{k}_energy.npy')
      energy_grids.append(grid)


n = len(energy_grids)
transfer_map = np.empty((n, n))

for i in range(n):
  acceptor = energy_grids[i]
  for j in range(n):
    donor = energy_grids[j]
    transfer_map[i,j] = transferability_coeff(donor, acceptor)
    #transfer_map[i,j] = average_difference(donor, acceptor)


# plotting
cm = 1 / 2.54
#fig, ax = plt.subplots(figsize=(38.0*cm, 30.4*cm))
fig, ax = plt.subplots(figsize=(26.0, 16.0))
ax.set_xlabel('Donor subgraph', fontsize='x-large')
ax.set_ylabel('Acceptor subgraph', fontsize='x-large')
img = ax.imshow(transfer_map, cmap='inferno', interpolation='nearest')  # transferability
#img = ax.imshow(transfer_map, cmap='inferno_r', interpolation='nearest')  # avg-diff
plt.colorbar(img)

# line seperators
location = -0.5  # seperator between pixels
ticks = []
labels = []
for x in [3, 4, 5]:
  for i in range(x):
    numbers = eval(f'ws_numbers_{x}reg{i}')
    location += len(numbers)
    if location < len(energy_grids) - 1:  # skip last lines
      ax.axvline(x=location, color='white', linestyle='--')
      ax.axhline(y=location, color='white', linestyle='--')

    ticks.append(location - len(numbers)/2)
    labels.append(f'{x}reg{i}')
    
plt.xticks(ticks, labels)
plt.yticks(ticks, labels)
ax.xaxis.tick_top()
plt.title('Transferability coefficients', fontsize='30', y=1.05)
plt.show()
#plt.savefig('transferability_map.pdf')
#fig.tight_layout()
#plt.savefig('difference_map.svg', bbox_inches='tight', format='svg', dpi=400)
