import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.algorithms import QAOA
from qiskit import Aer, execute, BasicAer

import networkx as nx
from networkx import Graph

import matplotlib.pyplot as plt
import os
import itertools

# custom functions
from circuit_generation import qaoa_circuit
from calculations import get_energy, get_energy_grid
from plotting import plot_energy


# Graph
G = Graph()
G.add_edges_from([(0,1),(1,2),(1,3),(2,3),(3,4)])
_edge = (1,3)  # edge to calculate energy from
#nx.draw_kamada_kawai(G, with_labels=True)

# circuit creation
qaoa_qc = qaoa_circuit(G, apx_sol=apx_sol, eps=0.1)
#qaoa_qc.draw('mpl')

# energy calculation
energy_grid = get_energy_grid(G, qaoa_qc, edge=_edge, samples=30)
#energy_grid = np.load('./paper-graphs/4-reg/3_energy.npy')
#print(get_energy(G, qaoa_qc, gamma=0.2*np.pi, beta=0.3*np.pi))

# plotting
plot_energy(energy_grid, title=apx_sol)
#np.save(f'./ws-energies/{name}_energy.npy', energy_grid)

#save_contents(G, qaoa_qc, energy_grid, name='3', folder='paper-graphs/4-reg')
