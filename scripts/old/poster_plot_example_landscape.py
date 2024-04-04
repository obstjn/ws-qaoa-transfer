import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from plotting import *
from graph_management import *


#ws = [0, 0, 0, 0, 0, 0]
ws = [1, 1, 0, 1, 0, 0]

energy = np.load(f'./ws-energies/3reg0/energies/{ws_to_number(ws, base=3)}_energy.npy')
plot_energy(energy, show=False)

plt.savefig('example_landscape1.svg', bbox_inches='tight', format='svg', dpi=400)
