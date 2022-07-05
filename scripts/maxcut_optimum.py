import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from plotting import *
from graph_management import *


# generate random graph
for i in range(200):
  Grand = nx.fast_gnp_random_graph(20, .25, seed=i)
  if nx.is_connected(Grand):
    print('seed =', i)
    break
else:  # executed if no break
  raise ValueError('No connected graph found!')
#Grand = nx.fast_gnp_random_graph(3, .25, seed=3)

np.random.seed(42)
# generate some random cuts
for i in range(6):
  gw_cut = ''.join(map(str, GW_maxcut(Grand)))[::-1]
  print(cut_value(Grand, gw_cut))

opt_cut = '00111001110111000011'
mc = maxcut(Grand)
print(mc, cut_value(Grand, mc))
#nx.draw_kamada_kawai(Grand, with_labels=True)
draw_graph_with_cut(Grand, opt_cut, draw_labels=True, show=False)
draw_graph_with_cut(Grand, gw_cut, draw_labels=True)
