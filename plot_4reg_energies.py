import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
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

confs0 = np.load('./ws-energies/ws-confs/4reg0_confs.npy')
confs1 = np.load('./ws-energies/ws-confs/4reg1_confs.npy')
confs2 = np.load('./ws-energies/ws-confs/4reg2_confs.npy')
confs3 = np.load('./ws-energies/ws-confs/4reg3_confs.npy')


configs = [confs0, confs1, confs2, confs3]
for i, conf in enumerate(configs):
  for apx in conf:
    energy = np.load(f'./ws-energies/4reg{i}/energies/{ws_to_number(apx)}_energy.npy')

    # plot graph
    draw_graph_with_ws(eval(f'G_4reg{i}'), warmstarting=apx, show=False)
    plt.savefig(f'./ws-energies/plots/graphs/4reg{i}/4reg{i}_ws_graph_{ws_to_number(apx)}.pdf')
    plt.close()

    # plot energy
    plot_energy(energy, title=str(apx), filename=f'./ws-energies/plots/energy-plots/4reg{i}/4reg{i}_{ws_to_number(apx)}')

