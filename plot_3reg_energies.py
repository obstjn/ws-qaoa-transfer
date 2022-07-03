import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from plotting import *
from graph_management import *


G_3reg0 = Graph()
G_3reg1 = Graph()
G_3reg2 = Graph()
G_3reg0.add_edges_from([(0,2), (1,2), (2,3), (3,4), (3,5)]) 
G_3reg1.add_edges_from([(0,1), (1,2), (1,3), (2,3), (3,4)])
G_3reg2.add_edges_from([(0,1), (0,2), (0,3), (1,3), (2,3)])

confs0 = np.load('./ws-energies/ws-confs/3reg0_confs.npy')
confs1 = np.load('./ws-energies/ws-confs/3reg1_confs.npy')
confs2 = np.load('./ws-energies/ws-confs/3reg2_confs.npy')

# remove entries containing 0.5
confs = []
for arr in confs0:
  if 0.5 in arr: continue
  confs.append(arr)
confs0 = np.array(confs)

confs = []
for arr in confs1:
  if 0.5 in arr: continue
  confs.append(arr)
confs1 = np.array(confs)

confs = []
for arr in confs2:
  if 0.5 in arr: continue
  confs.append(arr)
confs2 = np.array(confs)


configs = [confs0, confs1, confs2]
for i, apx in enumerate(configs):
  energy = np.load(f'./ws-energies/3reg{i}/energies/{ws_to_number(apx)}_energy.npy')
  draw_graph_with_ws(eval(f'G_3reg{i}'), warmstarting=apx, show=False)
  plt.savefig(f'3reg{i}_ws_graph_{ws_to_number(apx)}.pdf')
  plt.close()
  plot_energy(energy, title=str(apx), filename=f'3reg{i}_{ws_to_number(apx)}')
