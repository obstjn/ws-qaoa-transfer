import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from plotting import *
from graph_management import *
import random

from time import time


np.random.seed(5)
random.seed(40)
seq = [random.randint(1,5) for i in range(50)]
G = nx.random_degree_sequence_graph(seq, seed=42)

def load_landscape_from_graph(G, path='./energies/'):
  # (j-k)
  j = min(sg.degree(0), sg.degree(1))
  k = max(sg.degree(0), sg.degree(1))

  files = sorted(os.listdir(path))
  # filter files to check
  files = [file for file in files if f'({j}-{k})' in file]

  for file in files:
    G1, ws, grid = get_graph_ws_and_grid(path+file)

    # Prepare graphs
    # apply apx_sol
    attrs = {i: ws[i] for i in G1.nodes}
    nx.set_node_attributes(G1, attrs, 'weight')
    # mark central edge
    attrs = {e: 0 for e in G1.edges}
    attrs[(0,1)] = 1
    nx.set_edge_attributes(G1, attrs, 'central')

    G1_inverted = G1.copy()

    # Graph with inverse ws
    attrs_inv = {i: np.abs(ws[i]-1) for i in G1_inverted.nodes}
    nx.set_node_attributes(G1_inverted, attrs_inv, 'weight')

    # iso check
    comp = lambda g1, g2: g1['weight'] == g2['weight']
    ecomp = lambda g1, g2: g1['central'] == g2['central']
    if nx.is_isomorphic(G, G1, node_match=comp, edge_match=ecomp) or nx.is_isomorphic(G, G1_inverted, node_match=comp, edge_match=ecomp):  # found iso
      return grid

  # no iso found
  print(j, k)
  print(files)
  draw_graph_with_ws(G, show=True)

  
apx = GW_maxcut(G)
#print(cut_value(G, apx))

subgraphs = get_ws_subgraphs(G, apx)

true_energy = np.zeros((30, 30))

for sg, edge, occ in subgraphs:
  # print(occ)
  # draw_graph_with_ws(sg, draw_labels=False, show=True)
  grid = load_landscape_from_graph(sg)
  true_energy += occ * grid

plot_energy(true_energy)
  

exit()
#11x 4reg0 11 --> 19
# 9x 4reg0 10 --> 23

#for i, (subgraph, edge, occ) in enumerate(subgraphs):
#  print(i+1, occ)
#  draw_graph_with_ws(subgraph, show=False)
#plt.show()

apx_energy = np.zeros((30, 30))
apx_energy += 11 * np.load('./ws-energies/4reg0/energies/19_energy.npy')
apx_energy +=  9 * np.load('./ws-energies/4reg0/energies/23_energy.npy')

#plot_energy_with_marker(apx_energy, title='Approximate energy', show=False)
#plt.savefig('landscape-apx_apx-energy.pdf')

# subgraph type, ws_number (thesis notation), occurence
sg_data =[(0,11,11), (0,10,9), (0,17,3), (0,4,1), (0,18,1), (0,5,2), (0,16,1), (0,12,3), (0,8,2), (0,6,1), (1,4,2), (1,10,2), (1,9,2)]
true_energy = np.zeros((30,30))
for typ, ws, occ in sg_data:
  ws = ws_numbers[typ][ws]
  true_energy += occ * np.load(f'./ws-energies/{X}reg{typ}/energies/{ws}_energy.npy')

#plot_energy_with_marker(true_energy, title='True energy', show=False)
#plt.savefig('landscape-apx_true-energy.pdf')
#plt.show()