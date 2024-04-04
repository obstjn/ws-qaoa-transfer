import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from circuit_generation import *
from plotting import *
from graph_management import *

# 5-regular graphs
G_5reg0 = Graph()
G_5reg1 = Graph()
G_5reg2 = Graph()
G_5reg3 = Graph()
G_5reg4 = Graph()
G_5reg0.add_edges_from([(i,4) for i in range(4)] + [(4,5)] + [(5,j) for j in range(6,10)]) 
G_5reg1.add_edges_from([(0,3),(1,3),(2,3)] + [(3,4),(3,5),(4,5)] + [(5,6),(5,7),(5,8)])
G_5reg2.add_edges_from([(0,2),(1,2)] + [(2,3),(2,4),(2,5),(3,5),(4,5)] + [(5,6),(5,7)])
G_5reg3.add_edges_from([(0,1)] + [(1,2),(1,3),(1,4),(1,5)] + [(2,5),(3,5),(4,5)] + [(5,6)])
G_5reg4.add_edges_from([(0,i) for i in range(1,6)] + [(i,5) for i in range(1,5)])


Graphs = [G_5reg0, G_5reg1, G_5reg2, G_5reg3, G_5reg4]
edges = [(4,5), (3,5), (2,5), (1,5), (0,5)]

for i, G in enumerate(Graphs):
  # generate energy
  qc = qaoa_circuit(G)
  energy = get_energy_grid(G, qc, edges[i])
  np.save(f'./ws-energies/5reg{i}/5reg{i}_standard_energy.npy', energy)
  
  # plot landscapes
  energy = np.load(f'./ws-energies/5reg{i}/5reg{i}_standard_energy.npy')
  plot_energy(energy, filename=f'5reg{i}_standard')
