import networkx as nx
from plotting import *
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edges_from([(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (0,2), (1,4), (3,5)])
cut = '001011'
nc = node_color_mapping(G, cut)
ec = edge_color_mapping(G, cut)
nx.draw_circular(G, node_color=nc, edge_color=ec, width=1.4)
plt.savefig('maxCut_example.pdf')
