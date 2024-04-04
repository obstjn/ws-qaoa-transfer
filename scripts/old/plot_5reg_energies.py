import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
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

confs0 = np.load('./ws-energies/ws-confs/5reg0_confs.npy')
confs1 = np.load('./ws-energies/ws-confs/5reg1_confs.npy')
confs2 = np.load('./ws-energies/ws-confs/5reg2_confs.npy')
confs3 = np.load('./ws-energies/ws-confs/5reg3_confs.npy')
confs4 = np.load('./ws-energies/ws-confs/5reg4_confs.npy')


configs = [confs0, confs1, confs2, confs3, confs4]
for i, conf in enumerate(configs):
  for apx in conf:
    energy = np.load(f'./ws-energies/5reg{i}/energies/{ws_to_number(apx)}_energy.npy')

    # plot graphs
    #draw_graph_with_ws(eval(f'G_5reg{i}'), warmstarting=apx, show=False)
    #plt.savefig(f'./ws-energies/plots/graphs/5reg{i}/5reg{i}_ws_graph_{ws_to_number(apx)}.pdf')
    #plt.close()

    # plot energy
    plot_energy(energy, title=str(apx), filename=f'./ws-energies/plots/energy-plots/5reg{i}/5reg{i}_{ws_to_number(apx)}')

