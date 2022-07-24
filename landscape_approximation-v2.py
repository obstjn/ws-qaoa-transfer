import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from circuit_generation import *
from plotting import *
from graph_management import *

from qiskit.visualization import plot_histogram
from qiskit import Aer, execute


ws_numbers_4reg0 = [0, 1, 3, 7, 24, 25, 27, 33, 35, 57, 23, 19, 17, 8, 15, 11, 9, 51, 41, 43] 
ws_numbers_4reg1 = [0, 1, 3, 20, 21, 11, 8, 9, 28, 19, 17, 4, 7, 5, 25, 12, 13]               
ws_numbers = [ws_numbers_4reg0, ws_numbers_4reg1]

X = 4
np.random.seed(42)
G = nx.random_regular_graph(X, 20, seed=1234)
apx = GW_maxcut(G)
#print(''.join([str(b) for b in apx]))
#print(f'# edges: {len(G.edges())}')
#print(cut_value(G, apx))

#subgraphs = get_ws_subgraphs(G, apx)
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

