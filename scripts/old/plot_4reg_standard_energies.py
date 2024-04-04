import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from circuit_generation import *
from plotting import *
from graph_management import *

# 4-regular graphs
G_4reg0 = Graph()
G_4reg1 = Graph()
G_4reg2 = Graph()
G_4reg3 = Graph()
G_4reg0.add_edges_from([(i,3) for i in range(3)] + [(3,4)] + [(4,j) for j in range(5,8)])
G_4reg1.add_edges_from([(0,2),(1,2)] + [(2,3),(2,4),(3,4)] + [(4,5),(4,6)])
G_4reg2.add_edges_from([(0,1)] + [(1,2),(1,3),(1,4),(2,4),(3,4)] + [(4,5)])
G_4reg3.add_edges_from([(0,i) for i in range(1,5)] + [(i,4) for i in range(1,4)])

Graphs = [G_4reg0, G_4reg1, G_4reg2, G_4reg3]
edges = [(3,4), (2,4), (1,4), (0,4)]

for i, G in enumerate(Graphs):
  # generate energy
  qc = qaoa_circuit(G)
  energy = get_energy_grid(G, qc, edges[i])
  np.save(f'./ws-energies/4reg{i}/4reg{i}_standard_energy.npy', energy)
  
  # plot landscapes
  energy = np.load(f'./ws-energies/4reg{i}/4reg{i}_standard_energy.npy')
  plot_energy(energy, filename=f'4reg{i}_standard')
