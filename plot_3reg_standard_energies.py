import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from circuit_generation import *
from plotting import *
from graph_management import *

G_3reg0 = Graph()
G_3reg1 = Graph()
G_3reg2 = Graph()
G_3reg0.add_edges_from([(2,0), (3,0), (0,1), (1,4), (1,5)]) 
G_3reg1.add_edges_from([(2,0), (0,3), (0,1), (3,1), (1,4)])
G_3reg2.add_edges_from([(0,3), (0,2), (0,1), (3,1), (2,1)])

Graphs = [G_3reg0, G_3reg1, G_3reg2]

for i, G in enumerate(Graphs):
  # generate energy
  #qc = qaoa_circuit(G)
  #energy = get_energy_grid(G, qc, (0,1))
  #np.save(f'3reg{i}_standard_energy.npy', energy)
  
  # plot landscapes
  energy = np.load(f'./ws-energies/3reg{i}/3reg{i}_standard_energy.npy')
  plot_energy(energy, filename=f'3reg{i}_standard')
