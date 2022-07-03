import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from circuit_generation import *
from calculations import *
from plotting import *


G = nx.Graph()
G.add_weighted_edges_from([(0,1,2), (1,2,2), (1,3,3), (2,3,1), (3,4,1)])

# plot graph
#labels = nx.get_edge_attributes(G, 'weight')
#pos = nx.circular_layout(G)
#nx.draw(G, pos)
#nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
#plt.show()

#op = operator_from_graph(G)

#qc = qaoa_circuit(G)
#energy_grid = get_energy_grid(G, qc, (1,3), samples=65)
#np.save('./ws-energies/weighted-energies/test_energy.npy', energy_grid)
energy_grid = np.load('./ws-energies/weighted-energies/test_energy.npy')
plot_energy(energy_grid)
