import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from plotting import *

import os
from itertools import product


# 3-regular graphs
G_3reg0 = Graph()
G_3reg1 = Graph()
G_3reg2 = Graph()
G_3reg0.add_edges_from([(0,2), (1,2), (2,3), (3,4), (3,5)]) 
G_3reg1.add_edges_from([(0,1), (1,2), (1,3), (2,3), (3,4)])
G_3reg2.add_edges_from([(0,1), (0,2), (0,3), (1,3), (2,3)])

e_3reg0 = (2,3)
e_3reg1 = (1,3)
e_3reg2 = (0,3)

list_3reg = [(G_3reg0, e_3reg0), (G_3reg1, e_3reg1), (G_3reg2, e_3reg2)]


for i in range(3):
  folder = f'./ws-energies/3reg{i}/energies/'
  G, edge = list_3reg[i]
  
  for filename in sorted(os.listdir(folder)):
    # number of grid
    k = int(filename.split('_')[0])
    ws = number_to_ws(k, len(G), base=3)

    if ws[edge[0]] == 1 and ws[edge[1]] == 0 or ws[edge[0]] == 0 and ws[edge[1]] == 1:
      if .5 in ws:
        continue
      energy_grid = np.load(folder + f'{k}_energy.npy')
      plot_energy(energy_grid, title=str(ws), filename=f'./ws-energies/3reg_0-1_edge/only_0-1/3reg{i}_{k}')
