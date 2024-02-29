import matplotlib.pyplot as plt
import numpy as np
import os
import time

from circuit_generation import *
from calculations import *
from plotting import *
from graph_management import *


# ~~~~~~~~~~~~~~~ Graphs ~~~~~~~~~~~~~~~ #
# read graphs
graph_files = sorted(os.listdir('./test-run/graphs'))
graph_files = graph_files[16:]
graph_names = [fname.split('.')[0] for fname in graph_files]
graphs =[nx.read_adjlist(f'./test-run/graphs/{graph_fname}', nodetype=int) for graph_fname in graph_files]


# ~~~~~~~~~~~~~ Computation~~~~~~~~~~~~~~ #

# ~~~~~~~~~~~~~~ Progress ~~~~~~~~~~~~~~ #
# print('Start: ' + time.strftime('%H:%M:%S', time.localtime()), end='\n\n')
# print(f'Landscape total: {sum([len(get_relevant_warmstartings(G)) for G in graphs])}')
# k = 0

# ~~~~~~~~~~~~~ Calculation ~~~~~~~~~~~~ #
# grids = []
# for i, (G, graph_name) in enumerate(zip(graphs, graph_names)):
#     warmstartings = get_relevant_warmstartings(G)

#     for j, ws in enumerate(warmstartings):
#         ws_name = ''.join(map(str, ws))
#         # generate the circuit
#         qaoa_qc = qaoa_circuit(G, apx_sol=ws, eps=0.1)

#         # print progress
#         print(f'Graph {i+1}/{len(graphs)}: \t{graph_name}  \t ws {j+1}/{len(warmstartings)}: \t{ws_name} \t total: {k} \t{" "*20}')
#         k += 1
#         # calculate energy
#         grid = (get_energy_grid(G, qaoa_qc, edge=(0,1), gammaMax=2*np.pi, betaMax=np.pi, samples=30))
#         print('\r', end='\033[F\033[F')

#         # save results
#         grids.append(grid)
#         np.save(f'./test-run/energies/{graph_name}-{ws_name}.npy', grid)
# print('\n')
# print('Finished: ' + time.strftime('%H:%M:%S', time.localtime()))
    
# ~~~~~~~~~~~~~~~ Loading ~~~~~~~~~~~~~~ #
# Load grids from directory
grid_files = sorted(os.listdir('./test-run/energies'))
data = {}

# Loop through each grid file in the directory
for fname in grid_files:
    # Extract the grid name from the file name
    grid_name = fname.split('.')[0]

    # Load the grid array graph and warmstarting from the file
    grid = np.load(f'./test-run/energies/{fname}')
    G = nx.read_adjlist(f'./test-run/graphs/{fname[:7]}.graph', nodetype=int)
    ws = np.array(list(grid_name[8:]), dtype=int)

    # Add the tuple grid, graph, warmstarting to the data dictionary
    data[grid_name] = [grid, G, ws]


# ~~~~~~~~~~~~~~~ Plotting ~~~~~~~~~~~~~~ #
# plot grid
# for name, (grid, G, ws) in data.items():
#     if not name.startswith('(2-3)-0'):
#         continue
#     draw_landscape_and_graph(grid, G, warmstarting=ws, title=name)


# first = '(5-5)-0-0010001000'
# draw_landscape_and_graph(*data[first], title=first)
# second = '(3-3)-0-000000'
# draw_landscape_and_graph(*data[second], title=second)

# a = data[first][0]
# b = data[second][0]
# plot_energy(a-b)


# plot landscapes
# for energy, G, warmstarting in zip(grids, graphs, warmstartings):
#     ws = np.array([int(digit) for digit in warmstarting], dtype=int)
#     draw_landscape_and_graph(energy, G, ws)

test_files = ['./test-run/energies/' + f for f in grid_files if '(3-3)-0' in f] 
# G, ws, grid = get_graph_ws_and_grid(test_files[1])
# draw_landscape_and_graph(grid,G,ws)
draw_multiple_landscapes_and_graphs(test_files, rows=3, cols=4)

plt.show()