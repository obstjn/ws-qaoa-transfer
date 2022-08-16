import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from plotting import *
from graph_management import *
from calculations import *

G = Graph()
G.add_edges_from([(0,1),(0,2),(0,3),(1,2),(2,3),(3,4),(4,5),(4,6),(5,6),(5,7),(6,7),(1,7)])

#edge_list = [(0,2),(2,3),(1,2),(0,1),(0,3)]
edge_list = [(2,3),(0,2),(1,2),(3,4),(0,3)]
#edge_list = [(3,4),(2,3),(0,3),(4,5),(4,6)]
edge_colors = []
for edge in G.edges():
    if edge in edge_list:
        edge_colors.append('r')
    else:
        edge_colors.append('k')

#nx.draw_kamada_kawai(G, width=1.4)#, edge_color=edge_colors)

#G0 = nx.read_adjlist('./graphs/3reg0.graph', nodetype=int)
G1 = nx.read_adjlist('./graphs/3reg1.graph', nodetype=int)
#G2 = nx.read_adjlist('./graphs/3reg2.graph', nodetype=int)
#
#plt.figure()
#nx.draw_kamada_kawai(G0, width=1.4)#, edge_color=edge_colors)
#plt.savefig('3reg0.png')
#plt.figure()
#nx.draw_kamada_kawai(G1, width=1.4)#, edge_color=edge_colors)
#plt.savefig('3reg1.png')
#plt.figure()
#nx.draw_kamada_kawai(G2, width=1.4)#, edge_color=edge_colors)
#plt.savefig('3reg2.png')


# warmstarting
warmstarting = GW_maxcut(G)
apx_sol = np.array(warmstarting)
attrs = {i: apx_sol[i] for i in range(len(apx_sol))}
nx.set_node_attributes(G, attrs, name='weight')

cmap = {0.: '#6b00c2', .5: '#1f78b4', 1.: '#ffd500'}
colors = [cmap[G.nodes[n]['weight']] for n in G.nodes]
plt.figure()
nx.draw_kamada_kawai(G, with_labels=False, node_color=colors, font_color='k', width=1.4, edge_color=edge_colors)
#plt.show()
plt.savefig('3reg_graph_ws.png')

