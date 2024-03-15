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

apx = GW_maxcut(G)
#print(cut_value(G, apx))

subgraphs = get_ws_subgraphs(G, apx, get_equivalents=False)
equivalents = get_ws_subgraphs(G, apx, get_equivalents=True)

true_energy = np.zeros((30, 30))
apx_energy = np.zeros((30, 30))
apx_energy_thresh = np.zeros((30, 30))

for sg, edge, occ in subgraphs:
  # print(occ)
  # draw_graph_with_ws(sg, draw_labels=False, show=False)
  grid = load_landscape_from_graph(sg)
  true_energy += occ * grid

# plot_energy(true_energy, show=False, title='True Energy')

for sg, edge, occ in equivalents:
  grid = load_landscape_from_graph(sg)
  apx_energy += occ * grid

# plot_energy(apx_energy, show=False, title='Approximate Energy')

for sg, edge, occ in equivalents:
  if occ < 9:
    continue
  grid = load_landscape_from_graph(sg)
  apx_energy_thresh += occ * grid

# plot_energy(apx_energy_thresh, show=False, title='Energy of Top 3')

# plot_energy(true_energy - apx_energy, show=False, title='difference')


fig = plt.figure(figsize=(7.166, 2.2))
# plt.subplots_adjust(left=0.07, right=0.94, top=1.0, bottom=0.05, wspace=0.6)  # column config
plt.subplots_adjust(left=0.0, right=0.96, top=0.94, bottom=0.09, wspace=0.5)  # page config
ax1 = fig.add_subplot(1, 4, 1)
ax1.set_aspect(0.8)
ax2 = fig.add_subplot(1, 4, 2)
ax3 = fig.add_subplot(1, 4, 3)
ax4 = fig.add_subplot(1, 4, 4)
options = {'ax': ax1, 'node_size': 20}
draw_graph_with_cut(G, apx, show=False, **options)
plot_energy(true_energy, axes=ax2, show=False, title='True Energy')
plot_energy(apx_energy, axes=ax3, show=False, title='Approximate Energy')
plot_energy(apx_energy_thresh, axes=ax4, show=False, title='Energy of Top 3')
  
# plt.savefig('landscape_approximation.pdf')
plt.show()