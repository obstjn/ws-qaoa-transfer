import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from plotting import *
from graph_management import *
from calculations import *

def _draw_graph_with_ws(G, warmstarting=None, draw_labels=True, show=True):
  if warmstarting is not None:
    if len(warmstarting) != len(G):
      raise ValueError('Invalid warmstarting for the given graph!')
    apx_sol = np.array(warmstarting)
    attrs = {i: apx_sol[i] for i in range(len(apx_sol))}
    nx.set_node_attributes(G, attrs, name='weight')

  # plotting
  cmap = {0.: '#6b00c2', .5: '#1f78b4', 1.: '#ffd500'}
  colors = [cmap[G.nodes[n]['weight']] for n in G.nodes]
  plt.figure(figsize=[5.2, 4.8])
  nx.draw_kamada_kawai(G, with_labels=draw_labels, node_color=colors, font_color='k', width=1.4, node_size=1600)
  if show:
    plt.show()
  else:
    pass

G = nx.read_adjlist('./graphs/3reg0.graph', nodetype=int)
#ws = [0, 0, 0, 0, 0, 0]
ws = [1, 1, 0, 1, 0, 0]

_draw_graph_with_ws(G, warmstarting=ws, draw_labels=False, show=False)
#plt.savefig('example_graph0.svg', bbox_inches='tight', format='svg', dpi=400)
plt.savefig('example_graph1.svg', bbox_inches='tight', format='svg', dpi=400)
