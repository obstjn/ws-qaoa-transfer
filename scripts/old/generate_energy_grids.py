import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from circuit_generation import qaoa_circuit
from calculations import get_energy, get_energy_grid
from graph_management import *

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

# 4-regular graphs
G_4reg0 = Graph()
G_4reg1 = Graph()
G_4reg2 = Graph()
G_4reg3 = Graph()
G_4reg0.add_edges_from([(i,3) for i in range(3)] + [(3,4)] + [(4,j) for j in range(5,8)]) 
G_4reg1.add_edges_from([(0,2),(1,2)] + [(2,3),(2,4),(3,4)] + [(4,5),(4,6)])
G_4reg2.add_edges_from([(0,1)] + [(1,2),(1,3),(1,4),(2,4),(3,4)] + [(4,5)])
G_4reg3.add_edges_from([(0,i) for i in range(1,5)] + [(i,4) for i in range(1,4)])

e_4reg0 = (3,4)
e_4reg1 = (2,4)
e_4reg2 = (1,4)
e_4reg3 = (0,4)

list_4reg = [(G_4reg0, e_4reg0), (G_4reg1, e_4reg1), (G_4reg2, e_4reg2), (G_4reg3, e_4reg3)]

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

e_5reg0 = (4,5)
e_5reg1 = (3,5)
e_5reg2 = (2,5)
e_5reg3 = (1,5)
e_5reg4 = (0,5)

list_5reg = [(G_5reg0, e_5reg0), (G_5reg1, e_5reg1), (G_5reg2, e_5reg2), (G_5reg3, e_5reg3), (G_5reg4, e_5reg4)]

"""
# calculate the configurations/eliminate duplicates
iso_dict = {}
confs = []
k = 0
g = eval(f'G_4reg{k}')

for apx_sol in product([0, 1], repeat=len(g)):
    ws = np.array(apx_sol[::-1])

    if iso_in_dict(g, ws, iso_dict) or iso_in_dict(g, np.abs(ws-1), iso_dict):
        continue
    else:
        # hash of the warm start
        ws_hash = ws_hashing(ws)

        # check if hash is in dict
        if ws_hash in iso_dict.keys():
            iso_dict[ws_hash].append(ws)
        else:
            iso_dict[ws_hash] = [ws]
        confs.append(ws)
        
    # last conf to check
    if np.all(ws == 0.5):
        break

# check duplicates/isos
for i in range(len(confs)):
    for j in range(i+1, len(confs)):
        if np.allclose(np.abs(confs[i]-1)[::-1], confs[j]):
            print(confs[i], confs[j])

confs = np.array(confs)
np.save(f'./ws-energies/ws-confs/4reg{k}_confs.npy', confs)
print(len(confs))
"""

k = 0

# get relevant confs
confs = np.load(f'./ws-energies/ws-confs/4reg{k}_confs.npy')
print(len(confs))

# calculate energy grids
g, e = list_4reg[k]

for apx_sol in confs:
    n = ws_to_number(apx_sol, base=2)
    if n not in [23, 43, 51]:
      continue
    print(n)

    qaoa_qc = qaoa_circuit(g, apx_sol, eps=.1)

    energy_grid = get_energy_grid(g, qaoa_qc, e, samples=30)
    np.save(f'./ws-energies/4reg{k}/energies/{int(n)}_energy.npy', energy_grid)
