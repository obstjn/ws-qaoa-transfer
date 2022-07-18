import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from circuit_generation import *
from plotting import *
from graph_management import *
from scipy.optimize import minimize


X = 5
np.random.seed(42)
# generate random X-regular donor graph (20 nodes)
# calculate GW approximation for warm-start
G_donor = nx.random_regular_graph(X, 20, seed=0)

# calculate approximation and true maxcut
apx_donor = GW_maxcut(G_donor)
draw_graph_with_cut(G_donor, apx_donor, draw_labels=True)
maxcut_donor = maxcut(G_donor)
maxval_donor = cut_value(G_donor, maxcut_donor)  # =26  # =32  # =42
#apxval_donor = cut_value(G_donor, apx_donor)  # = 25  # =32  # =40


# show subgraphs
#for (subgraph, edge, occurence) in get_ws_subgraphs(G_donor, apx_donor):
#  print(occurence)
#  draw_graph_with_ws(subgraph, show=False)
#plt.show()

# subgraph type, ws_number, occurence
sg_data3 = [(0,182,2), (1,60,3), (1,56,6), (0,56,10), (0,62,7), (0,72,2)]  # 3reg
sg_data4 = [(1,19,6), (0,19,10), (0,23,3), (0,51,7), (1,20,3), (1,25,2), (0,25,2), (0,41,2), (0,24,1), (1,17,2), (1,21,2)]  # 4reg
sg_data5 = [(0,211,3), (0,99,4), (1,41,4), (1,35,2), (0,113,2), (0,35,1), (0,49,2), (0,103,6), (0,39,10), (1,39,4), (0,47,4), (1,49,1), (1,40,1), (1,51,4), (2,36,1), (3,37,1)]  # 5reg

# calculate the optimal parameters (warm-started)
# energy from subgraphs
donor_energy = np.zeros((30,30))
for typ, ws, occ in eval(f'sg_data{X}'):
  donor_energy += occ * np.load(f'./ws-energies/{X}reg{typ}/energies/{ws}_energy.npy')
  
#plot_energy(donor_energy)
#gam, bet = maximizing_parameters(donor_energy, plotting=False)
#gam = gam[0]
#bet = bet[0]
#maxenergy_donor = np.max(donor_energy)
#print(f'maximum energy donor: {maxenergy_donor}')
#print(f'maxcut value donor:   {maxval_donor}')
#print(f'apx ratio of donor:   {maxenergy_donor/maxval_donor}')
#print()
#print('maximizing parameters')
#print(f'gamma: {gam}, beta: {bet}')

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

# for low parameter transfer
def anti_objective_function_ws(params, *args):
  return -objective_function_ws(params, *args)

# optimize parameters
#np.random.seed(42)
#print('\noptimization:')
#xinit = np.array([gam, bet])
#optimized_result = minimize(objective_function_ws, x0=xinit, method='COBYLA', args=(G_donor, apx_donor, get_ws_subgraphs(G_donor, apx_donor)))
#gam = optimized_result.x[0]
#bet = optimized_result.x[1]
#print()
#print(optimized_result)
#print(f'\noptimized apx ratio: {-optimized_result.fun/maxval_donor}')


## high parameter transfer
#apx_cuts = []
#opt_cuts = []
#opt_values = []
#opt_energies = []  # these are the energies using optimized energy parameters of donor (not optimal energy of acceptor)
#print('\napx ratio acceptors:')
#np.random.seed(42)
#for i in range(30):
#  # generate 30 acceptor graphs
#  G_acceptor = nx.random_regular_graph(X, 20, seed=i+1)
#  # calculate GW approximation
#  apx_acc = GW_maxcut(G_acceptor)
#
#  # use parameters to get the energy of each graph
#  qc = qaoa_circuit(G_acceptor, apx_sol=apx_acc, eps=0.1)
#  energy = get_energy(G_acceptor, qc, gam, bet, None, shots=1)
#  
#  # calculate approximation ratios
#  opt_cut = maxcut(G_acceptor)
#  opt_val = cut_value(G_acceptor, opt_cut)
#
#  # write to list
#  apx_cuts.append(apx_acc)
#  opt_cuts.append(opt_cut)
#  opt_values.append(opt_val)
#  opt_energies.append(energy)
#
#  print(energy/opt_val)
#  
## save results
#apx_cuts = np.array(apx_cuts)
#opt_cuts = np.array(opt_cuts)
#opt_values = np.array(opt_values)
#opt_energies = np.array(opt_energies)
#np.save(f'./scripts/data-stash/{X}reg/apx_cuts.npy', apx_cuts)
#np.save(f'./scripts/data-stash/{X}reg/opt_cuts.npy', opt_cuts)
#np.save(f'./scripts/data-stash/{X}reg/opt_values.npy', opt_values)
#np.save(f'./scripts/data-stash/{X}reg/opt_energies.npy', opt_energies)


# random parameters
#apx_cuts = np.load(f'./scripts/data-stash/{X}reg/apx_cuts.npy')
#opt_values = np.load(f'./scripts/data-stash/{X}reg/opt_values.npy')
#rand_energies = []
#print('\nrandom apx ratio acceptors:')
#np.random.seed(42)
#for i in range(30):
#  # generate 30 acceptor graphs
#  G_acceptor = nx.random_regular_graph(X, 20, seed=i+1)
#  # calculate GW approximation
#  apx_acc = apx_cuts[i]
#  # random parameters
#  gam, bet = np.random.rand(2) * np.array([2*np.pi, np.pi])
#
#  # use parameters to get the energy of each graph
#  qc = qaoa_circuit(G_acceptor, apx_sol=apx_acc, eps=0.1)
#  rand_energy = get_energy(G_acceptor, qc, gam, bet, None, shots=1)
#  
#  # calculate approximation ratios
#  opt_val = opt_values[i]
#
#  # write to list
#  rand_energies.append(rand_energy)
#
#  print(rand_energy/opt_val)
#
#rand_energies = np.array(rand_energies)
#np.save(f'./scripts/data-stash/{X}reg/rand_energies.npy', rand_energies)


# deoptimize parameters
#gam, bet = np.where(donor_energy <= donor_energy.min() + 1e-5)
#gam = gam[0]
#bet = bet[0]
#gam *= 2*np.pi / donor_energy.shape[0]
#bet *= np.pi / donor_energy.shape[1]
#print(f'minimum energy donor:   {donor_energy.min()}')
#print(f'maxcut value donor:     {maxval_donor}')
#print(f'min apx ratio of donor: {donor_energy.min()/maxval_donor}')
#print()
#print('minimizing parameters')
#print(f'gamma: {gam}, beta: {bet}')
#
#print('\ndeoptimization:')
#xinit = np.array([gam, bet])
#np.random.seed(42)
#deoptimized_result = minimize(anti_objective_function_ws, x0=xinit, method='COBYLA', args=(G_donor, apx_donor, get_ws_subgraphs(G_donor, apx_donor)))
#gam = deoptimized_result.x[0]
#bet = deoptimized_result.x[1]
#print()
#print(deoptimized_result)
#print(f'\ndeoptimized apx ratio: {deoptimized_result.fun/maxval_donor}')
#
#apx_cuts = np.load(f'./scripts/data-stash/{X}reg/apx_cuts.npy')
#opt_values = np.load(f'./scripts/data-stash/{X}reg/opt_values.npy')
#deopt_energies = []  # deoptimized energies
#print('\napx ratio acceptors:')
#np.random.seed(42)
#for i in range(30):
#  # generate 30 acceptor graphs
#  G_acceptor = nx.random_regular_graph(X, 20, seed=i+1)
#  # calculate GW approximation
#  apx_acc = apx_cuts[i]
#
#  # use parameters to get the energy of each graph
#  qc = qaoa_circuit(G_acceptor, apx_sol=apx_acc, eps=0.1)
#  energy = get_energy(G_acceptor, qc, gam, bet, None, shots=1)
#  
#  # calculate approximation ratios
#  opt_val = opt_values[i]
#
#  # write to list
#  deopt_energies.append(energy)
#
#  print(energy/opt_val)
#  
## save results
#deopt_energies = np.array(deopt_energies)
#np.save(f'./scripts/data-stash/{X}reg/deopt_energies.npy', deopt_energies)
