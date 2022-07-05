import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from circuit_generation import qaoa_circuit
from calculations import get_energy, get_energy_grid
from plotting import plot_energy, draw_graph_with_ws
from graph_management import number_to_ws, ws_to_number, get_ws_from_attributes, get_reg0_equivalent


def get_ws_subgraphs(G, apx_sol):
  subgraphs = []

  """ ~~~~~~~~~ """
  G3reg0 = Graph()
  G3reg0.add_edges_from([(0,2), (1,2), (2,3), (3,4), (3,5)])
  warmstarts = np.load('./ws-energies/ws-confs/confs_with_0.5/3reg0_confs.npy')
  graphs0 = []

  for ws in warmstarts:
    Gws = G3reg0.copy()
    number = ws_to_number(ws)
    attrs = {i: ws[i] for i in range(len(ws))}
    nx.set_node_attributes(Gws, attrs, name='weight')
    graphs0.append((Gws, number))

  G3reg1 = Graph()
  G3reg1.add_edges_from([(0,1), (1,2), (1,3), (2,3), (3,4)])
  warmstarts = np.load('./ws-energies/ws-confs/3reg1_confs.npy')
  graphs1 = []

  for ws in warmstarts:
    Gws = G3reg1.copy()
    number = ws_to_number(ws)
    attrs = {i: ws[i] for i in range(len(ws))}
    nx.set_node_attributes(Gws, attrs, name='weight')
    graphs1.append((Gws, number))

  graphs = {6: graphs0, 5: graphs1}
  len_to_reg = {6: 0, 5: 1, 4: 2}  # used to find appropriate 3reg graph (class) based on number of nodes

  """ ~~~~~~~~~ """

  total = np.zeros((30,30))
  for edge in G.edges():
    u, v = edge
    subgraph = Graph()
    subgraph.add_edge(u,v)
    subgraph.add_edges_from([(u,n) for n in G.neighbors(u)])
    subgraph.add_edges_from([(v,n) for n in G.neighbors(v)])

    attrs = {i: apx_sol[i] for i in subgraph.nodes}
    nx.set_node_attributes(subgraph, attrs, 'weight')
    draw_graph_with_ws(subgraph, show=False)

    subgraph = get_reg0_equivalent(subgraph)
    subgraph = nx.convert_node_labels_to_integers(subgraph)
    draw_graph_with_ws(subgraph)

    apx = get_ws_from_attributes(subgraph)

    # iso check
    comp = lambda g1, g2: g1['weight'] == g2['weight']
    for item in graphs[len(subgraph)]:
      graph, number = item
      if nx.is_isomorphic(subgraph, graph, node_match=comp):  # found iso
        grid = np.load(f'./ws-energies/3reg{len_to_reg[len(subgraph)]}/energies/{number}_energy.npy')
        break
    else:  # executed if no break
      #check inverted ws
      attrs_comp = {i: np.abs(apx[i]-1) for i in subgraph.nodes}  # inverse warm starting
      nx.set_node_attributes(subgraph, attrs_comp, 'weight')
      for item in graphs[len(subgraph)]:
        graph, number = item
        if nx.is_isomorphic(subgraph, graph, node_match=comp):  # found iso
          grid = np.load(f'./ws-energies/3reg{len_to_reg[len(subgraph)]}/energies/{number}_energy.npy')
          break
      else:  # execute if no break
        print(get_ws_from_attributes(subgraph))
        draw_graph_with_ws(subgraph)
        print('ERROR!')

    total += grid
  plot_energy(total)  

  return None

# warm starting
apxsol = np.array([0,1,0,1,0,1,0,1])
G3 = nx.random_regular_graph(3, 8, seed=42)

# plot
#draw_graph_with_ws(G3, apxsol)

subgraphs = get_ws_subgraphs(G3, apxsol)
