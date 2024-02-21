import numpy as np
import networkx as nx
from networkx import Graph
from itertools import product


def iso_in_dict(G1, apx_sol1, iso_dict):
  # preselect relevant graphs with ws_hash (same # of 0s, ...)
  ws_hash = ws_hashing(apx_sol1)

  if ws_hash in iso_dict.keys():
    # add approximate solution to G1 as 'weight'
    attrs = {i: apx_sol1[i] for i in range(len(apx_sol1))}
    nx.set_node_attributes(G1, attrs, 'weight')
    # Graph to compare to 
    G2 = Graph()
    G2.add_edges_from(G1.edges())

    # check every candidate for isomorphism
    for apx_sol2 in iso_dict[ws_hash]:
      # add approximate solution to G2 as 'weight'
      attrs = {i: apx_sol2[i] for i in range(len(apx_sol2))}
      nx.set_node_attributes(G2, attrs, 'weight')

      # isomorphism check
      comp = lambda g1, g2: g1['weight'] == g2['weight']
      if nx.is_isomorphic(G1, G2, node_match=comp):
        # found iso
        return True

    # found no iso
    return False
  else:
    # no candidate
    return False


def ws_hashing(apx_sol):
  """ number of 0s and ones in tuple [0, 0, 1] --> (2, 1) """
  ws_hash = (np.count_nonzero(apx_sol == 0.),
             np.count_nonzero(apx_sol == 1.))
  return ws_hash


def number_to_ws(n, l, base=2):
    """
    Gives the warm start corresponding to a certain number.
    Index 0 is warm starting of node 0
    l is the length of the warm start i.e. number of nodes.
    """
    if n == 0:
        return np.array([0]*l)
    digits = []
    while n:
        digits.append(int(n % base))
        n //= base
    # pad with zeros
    digits.extend([0]*(l-len(digits)))
    return np.array(digits) / (base - 1)


def ws_to_number(apx_sol, base=2):
    return int(sum([(base-1)*apx_sol[i] * base**i for i in range(len(apx_sol))]))


def get_ws_from_attributes(G):
    apx = np.array([ws for n, ws in nx.get_node_attributes(G, 'weight').items()])
    return apx


def split_node(G, node):
  """ https://stackoverflow.com/questions/65853641/networkx-how-to-split-nodes-into-two-effectively-disconnecting-edges """
  edges = G.edges(node, data=True)
  ws_value = G.nodes[node]['weight']
  
  new_edges = []
  new_nodes = []

  H = G.__class__()
  H.add_nodes_from(G.subgraph(node))
  
  for i, (s, t, data) in enumerate(edges):
      new_node = '{}_{}'.format(node, i)
      I = nx.relabel_nodes(H, {node:new_node})
      new_nodes += list(I.nodes(data=True))
      new_edges.append((new_node, t, data))
  
  G.remove_node(node)
  G.add_nodes_from(new_nodes, weight=ws_value)
  G.add_edges_from(new_edges)
  
  return nx.convert_node_labels_to_integers(G)


def get_reg0_equivalent(G):
  G_eq = G.copy()
  for node in G.nodes:
    if G_eq.degree(node) == 2:
      G_eq = split_node(G_eq, node)
  return G_eq


def get_subgraphs(G):
  subgraphs = []

  for edge in G.edges():
    u, v = edge
    subgraph = Graph()
    subgraph.add_edge(u,v)
    subgraph.add_edges_from([(u,n) for n in G.neighbors(u)])
    subgraph.add_edges_from([(v,n) for n in G.neighbors(v)])
    subgraph = nx.convert_node_labels_to_integers(subgraph)

    # iso check
    for item in subgraphs:
      sg, edge, occurrence = item
      # found iso
      if nx.is_isomorphic(subgraph, sg):
        item[2] += 1  # increase occurrence by one
        break
    else:  # executed if no break
      edge = (0,1)
      subgraphs.append([subgraph, edge, 1])
    
  return subgraphs


def get_ws_subgraphs(G, apx_sol):
  """ returns a tuple of (subgraph, relevant-edge, occurence) """
  subgraphs = []

  for edge in G.edges():
    u, v = edge
    subgraph = Graph()
    subgraph.add_edge(u,v)
    subgraph.add_edges_from([(u,n) for n in G.neighbors(u)])
    subgraph.add_edges_from([(v,n) for n in G.neighbors(v)])

    inverted_sg = subgraph.copy()

    attrs = {i: apx_sol[i] for i in subgraph.nodes}
    nx.set_node_attributes(subgraph, attrs, 'weight')

    # subgraph with inverse apx_sol
    attrs_inv = {i: np.abs(apx_sol[i]-1) for i in inverted_sg.nodes}
    nx.set_node_attributes(inverted_sg, attrs_inv, 'weight')

    # normalize labels
    subgraph = nx.convert_node_labels_to_integers(subgraph)
    inverted_sg = nx.convert_node_labels_to_integers(inverted_sg)

    # iso check
    comp = lambda g1, g2: g1['weight'] == g2['weight']
    for item in subgraphs:
      sg, edge, occurrence = item
      if nx.is_isomorphic(subgraph, sg, node_match=comp) or nx.is_isomorphic(inverted_sg, sg, node_match=comp):  # found iso
        item[2] += 1  # increase occurrence by one
        break
    else:  # executed if no break
      edge = (0,1)
      subgraphs.append([subgraph, edge, 1])
    
  return subgraphs


def get_relevant_warmstartings(G):
  """ get all warmstartings for graph G up to isomorphism """
  iso_dict = {}  # stores the graphs with in a simple hash table
  warmstartings = []
  candidates = list(product([0, 1], repeat=len(G)))
  # only check the first half, as all other are isos
  candidates = candidates[:len(candidates)//2]

  for apx_sol in candidates:
      ws = np.array(apx_sol[::-1])

      if iso_in_dict(G, ws, iso_dict) or iso_in_dict(G, np.abs(ws-1), iso_dict):
          continue
      else:
          # hash of the warm start
          ws_hash = ws_hashing(ws)

          # check if hash is in dict
          if ws_hash in iso_dict.keys():
              iso_dict[ws_hash].append(ws)
          else:
              iso_dict[ws_hash] = [ws]
          warmstartings.append(ws)
          
  warmstartings = np.array(warmstartings)

  return warmstartings


def generate_graph(left_degree: int, right_degree: int, num_merged_nodes: int) -> nx.Graph:
    """
    Generate a graph with a central edge. The central node is
    connected to `left_degree` nodes on one side and `right_degree` nodes
    on the other side. The number `num_merged_nodes` gives the number of
    nodes that will be merged.

    Input:
    ----------
    left_degree: int, the number of nodes connected to the central node
    on the left side of the graph.
    right_degree: int, the number of nodes connected to the central node
    on the right side of the graph.
    num_merged_nodes: int, the number of nodes to be merged.

    Output:
    ----------
    Graph:  A Graph instance representing the generated graph.

    Note: The graph is generated by creating a central edge, and
    then adding `left_degree` nodes on one side and `right_degree` nodes
    on the other side.
    """

    # Create a Graph object to represent the graph.
    G = Graph()

    # Create the central edge between the two nodes.
    edges = [(0, 1)]  

    # Add the left neighbors of the central node to the graph.
    edges.extend([(0, k+2) for k in range(left_degree)]) 

    # Reuse existing nodes for edges
    n = left_degree + 2 - num_merged_nodes

    # Add the right neighbors of the central node to the graph.
    edges.extend([(1, k+n) for k in range(right_degree)]) 

    # Add all the edges to the graph.
    G.add_edges_from(edges)
    nx.convert_node_labels_to_integers(G)

    return G
