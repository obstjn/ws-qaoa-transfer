import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from circuit_generation import *
from plotting import *
from graph_management import *
from scipy.optimize import minimize


np.random.seed(42)
# generate random 3-regular donor graph (20 nodes)
# calculate GW approximation for warm-start
G_donor = nx.random_regular_graph(3, 20, seed=0)

apx_donor = GW_maxcut(G_donor)
maxcut_donor = maxcut(G_donor)
maxval_donor = cut_value(G_donor, maxcut_donor)
apxval_donor = cut_value(G_donor, apx_donor)

# subgraph type, ws_number, occurence
sg_data = [(0,182,2), (1,60,3), (1,56,6), (0,56,10), (0,62,7), (0,72,2)]

# calculate the optimal parameters (warm-started)
#for (subgraph, edge, occurence) in get_ws_subgraphs(G_donor, apx_donor):
#  print(occurence)
#  draw_graph_with_ws(subgraph)
energy = np.zeros((30,30))
for typ, ws, occ in sg_data:
  energy += occ * np.load(f'./ws-energies/3reg{typ}/energies/{ws}_energy.npy')
  
#plot_energy(energy)
gam, bet = maximizing_parameters(energy, plotting=False)
gam = gam[0]
bet = bet[0]
maxenergy_donor = np.max(energy)
print(f'maxcut value: {maxval_donor}')
print(f'maximum energy donor: {maxenergy_donor}')
print(f'apx ratio of donor: {maxenergy_donor/maxval_donor}')
print()
print('maximizing parameters')
print(f'gamma: {gam}, beta: {bet}')

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

# optimize
#xinit = np.array([gam, bet])
#optimized_result = minimize(objective_function_ws, x0=xinit, method='COBYLA', args=(G_donor, apx_donor, get_ws_subgraphs(G_donor, apx_donor)))
#gam = optimized_result.x[0]
#bet = optimized_result.x[1]
#print()
#print(optimized_result)
#print(f'optimized apx ratio: {-optimized_result.fun/maxval_donor}')


print('\napx ratio acceptors:')
for i in range(5):
  # generate 25 acceptor graphs
  G_acceptor = nx.random_regular_graph(3, 20, seed=i+1)
  # calculate GW approximation
  apx_acc = GW_maxcut(G_acceptor)

  # use parameters to get the energy of each graph
  qc = qaoa_circuit(G_acceptor, apx_sol=apx_acc, eps=0.1)
  energy = get_energy(G_acceptor, qc, gam, bet, None, shots=1)
  
  # calculate approximation ratios
  opt_cut = maxcut(G_acceptor)
  opt_val = cut_value(G_acceptor, opt_cut)

  print(energy/opt_val)
