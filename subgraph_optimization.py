import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from circuit_generation import qaoa_circuit
from calculations import get_energy, get_energy_grid
from plotting import plot_energy, draw_graph_with_ws
from graph_management import *

""" normal 3reg graph """
def objective_function(params, *args):
  G = args[0]
  subgraphs = get_subgraphs(G)
  energies = []
  grid = np.zeros((64,64))
  gamma, beta = params

  for item in subgraphs:
    subgraph, edge, occurrence = item
    qc = qaoa_circuit(subgraph)

    energies.append(occurrence * get_energy(subgraph, qc, gamma, beta, edge, shots=1))
    #grid += get_energy_grid(subgraph, qc, edge, samples=64) * occurrence

  return -sum(energies)


G3 = nx.random_regular_graph(3, 8, seed=42)
#print(objective_function([.717, .432], (G3)))

np.random.seed(42)
xinit = np.random.rand(2) * np.array([2*np.pi, np.pi])
xinit = np.array([2.7, 1.2])

path = [xinit]
def save_path(x):
  path.append(x)

# no warm starting
#optimized_result = minimize(objective_function, x0=xinit, method='COBYLA', args=(G3), callback=save_path)
#print(optimized_result)
#
#grid = np.load('./ws-energies/subgraph-optimization/energy_test.npy')
#plot_energy(grid, show=False)
#
#g, b = zip(*path)
#plt.plot(b, g, '--')
#plt.scatter(optimized_result.x[1], optimized_result.x[0], s=120, linewidths=2.0, facecolors='none', color='red')
#plt.show()


""" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """

""" warm started 3reg graph """
def objective_function_ws(params, *args):
  G, apx_sol, subgraphs = args
  energies = []
  gamma, beta = params

  for item in subgraphs:
    subgraph, edge, occurrence = item
    apxsol = np.array([w for node, w in nx.get_node_attributes(subgraph, 'weight').items()])
    qc = qaoa_circuit(subgraph, apxsol, eps=.1)

    energies.append(occurrence * get_energy(subgraph, qc, gamma, beta, edge, shots=1))

  return -sum(energies)


# warm starting
#apxsol = np.array([0,1,0,1,0,1,0,1])
#subgraphs = get_ws_subgraphs(G3, apxsol)

# save energy landscape
#grid = np.zeros((24,24))
#for item in subgraphs:
#  subgraph, edge, occurrence = item
#  apxsol = np.array([w for node, w in nx.get_node_attributes(subgraph, 'weight').items()])
#  print(apxsol)
#  qc = qaoa_circuit(subgraph, apxsol, eps=.1)
#  grid += get_energy_grid(subgraph, qc, edge, samples=24) * occurrence
#np.save('./ws-energies/subgraph-optimization/energy_ws_test.npy', grid)
#grid = np.load('./ws-energies/subgraph-optimization/energy_ws_test.npy')
#plot_energy(grid)

# optimize
#optimized_result = minimize(objective_function_ws, x0=xinit, method='COBYLA', args=(G3, apxsol, subgraphs), callback=save_path)
#print(optimized_result)

# load & plot energy landscape
#grid = np.load('./ws-energies/subgraph-optimization/energy_ws_test.npy')
#plot_energy(grid, show=False)

# plot path
#g, b = zip(*path)
#plt.plot(b, g, '--')
#plt.scatter(xinit[1], xinit[0], s=120, linewidths=2.0, marker='x')
#plt.scatter(optimized_result.x[1], optimized_result.x[0], s=120, linewidths=2.0, facecolors='none', color='red')
#plt.show()

""" random graphs """
# generate random graph
for i in range(200):
  Grand = nx.fast_gnp_random_graph(8, .25, seed=i)
  if nx.is_connected(Grand):
    break
else:  # executed if no break
  raise ValueError('No connected graph found!')
Grand = nx.fast_gnp_random_graph(8, .25, seed=3)

# plot subgraphs
nx.draw_kamada_kawai(Grand, with_labels=False)
plt.show()
subgraphs = get_subgraphs(Grand)
for item in subgraphs:
  sg, edge, occurrence = item
  print(occurrence)
  nx.draw_kamada_kawai(sg, with_labels=False)
  plt.show()

## load & plot energy landscape
#grid = np.load('./ws-energies/subgraph-optimization/random-graph-energy.npy')
#plot_energy(grid, show=False)
#
#xinit = np.array([2.7, 1.2])
#np.random.seed(42)
#
## optimization
#skip = [3,5,6]
#for i in range(8):
#  xinit = np.random.rand(2) * np.array([2*np.pi, np.pi])
#  if i in skip: continue
#  path = [xinit]
#  optimized_result = minimize(objective_function, x0=xinit, method='COBYLA', args=(Grand), callback=save_path)
#  print()
#  print(optimized_result)
#  print(i)
#
#  # plot path
#  g, b = zip(*path)
#  plt.plot(b, g, '--')
#  plt.scatter(xinit[1], xinit[0], s=120, linewidths=2.0, marker='x')
#  plt.scatter(optimized_result.x[1], optimized_result.x[0], s=120, linewidths=2.0, facecolors='none', color='red')
#plt.savefig('subgraph_optimization.pdf')
#plt.show()
