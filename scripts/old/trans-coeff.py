import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt


from circuit_generation import *
from calculations import *
from plotting import *
from graph_management import *


energy_3reg0 = np.load('./ws-energies/3reg0/3reg0_standard_energy.npy')
energy_4reg0 = np.load('./ws-energies/4reg0/4reg0_standard_energy.npy')
energy_5reg0 = np.load('./ws-energies/5reg0/5reg0_standard_energy.npy')
energies = {3: energy_3reg0, 4: energy_4reg0, 5: energy_5reg0}

trans = np.empty((3,3))
diff = np.empty((3,3))

for i in [3,4,5]:
  acceptor_energy = energies[i]
  for j in [3,4,5]:
    donor_energy = energies[j]
    trans[i-3,j-3] = transferability_coeff(donor_energy, acceptor_energy)
    diff[i-3,j-3] = average_difference(donor_energy, acceptor_energy)
    

print(trans)
print()
print(diff)
