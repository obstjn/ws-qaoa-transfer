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


# ~~~~~~~~~~~~~~ Progress ~~~~~~~~~~~~~~ #
print('Start: ' + time.strftime('%H:%M:%S', time.localtime()), end='\n\n')
print(f'Landscape total: {sum([len(get_relevant_warmstartings(G)) for G in graphs])}')
k = 0

# ~~~~~~~~~~~~~ Calculation ~~~~~~~~~~~~ #
grids = []
for i, (G, graph_name) in enumerate(zip(graphs, graph_names)):
    warmstartings = get_relevant_warmstartings(G)

    for j, ws in enumerate(warmstartings):
        ws_name = ''.join(map(str, ws))
        # generate the circuit
        qaoa_qc = qaoa_circuit(G, apx_sol=ws, eps=0.1)

        # print progress
        print(f'Graph {i+1}/{len(graphs)}: \t{graph_name}  \t ws {j+1}/{len(warmstartings)}: \t{ws_name} \t total: {k} \t{" "*20}')
        k += 1
        # calculate energy
        grid = (get_energy_grid(G, qaoa_qc, edge=(0,1), gammaMax=2*np.pi, betaMax=np.pi, samples=30))
        print('\r', end='\033[F\033[F')

        # save results
        grids.append(grid)
        np.save(f'./test-run/energies/{graph_name}-{ws_name}_energy.npy', grid)
print('\n')
print('Finished: ' + time.strftime('%H:%M:%S', time.localtime()))
    
# load grids
# grid_files = sorted(os.listdir('./test-run/energies'))
# grid_names = [fname.split('.')[0][:-7] for fname in grid_files]  # crop '_energy'
# grids = [np.load(f'./test-run/energies/{fname}') for fname in grid_files]
# graphs = [nx.read_adjlist(f'./test-run/graphs/{graph_fname[:7]}.graph', nodetype=int) for graph_fname in grid_names]
# warmstartings = [name[8:] for name in grid_names]

# ~~~~~~~~~~~~~~~ Plotting ~~~~~~~~~~~~~~ #
# plot grid
# for energy_grid, G, name in zip(grids, graphs, graph_names):
#     draw_graph_with_ws(G, warmstarting=[0]*len(G), show=False)
#     plot_energy(energy_grid, gammaMax=2*np.pi, betaMax=np.pi, title=name, filename=None, show=True)

# plot landscapes
# for energy, G, warmstarting in zip(grids, graphs, warmstartings):
#     ws = np.array([int(digit) for digit in warmstarting], dtype=int)
#     draw_landscape_and_graph(energy, G, ws)