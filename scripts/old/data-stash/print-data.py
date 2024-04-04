import numpy as np
import networkx as nx

from calculations import *

X = 5
np.random.seed(42)
G_donor = nx.random_regular_graph(X, 20, seed=0)
# donor
apx_donor = GW_maxcut(G_donor)
maxcut_donor = maxcut(G_donor)
maxval_donor = cut_value(G_donor, maxcut_donor)  # =26  # =32  # =42
apxval_donor = cut_value(G_donor, apx_donor)  # = 25  # =32  # =40

print(f'0 & {"".join([str(i) for i in apx_donor])} & {apxval_donor} & {maxval_donor} &  & -  &   \\\\')

# instances
apx_cuts = np.load(f'./scripts/data-stash/{X}reg/apx_cuts.npy')
deopt_energies = np.load(f'./scripts/data-stash/{X}reg/deopt_energies.npy')
rand_energies = np.load(f'./scripts/data-stash/{X}reg/rand_energies.npy')
opt_energies = np.load(f'./scripts/data-stash/{X}reg/opt_energies.npy')
opt_values = np.load(f'./scripts/data-stash/{X}reg/opt_values.npy')
for i in range(30):
  G = nx.random_regular_graph(X, 20, seed=i+1)
  apx = apx_cuts[i]
  apxval = cut_value(G, apx)
  maxval = opt_values[i]
  deopt_energy = deopt_energies[i]
  rand_energy = rand_energies[i]
  opt_energy = opt_energies[i]

  print(f'{i+1} & {"".join([str(j) for j in apx])} & {apxval} & {maxval} & {deopt_energy/maxval:.3f} & {rand_energy/maxval:.3f} & {opt_energy/maxval:.3f}  \\\\')
