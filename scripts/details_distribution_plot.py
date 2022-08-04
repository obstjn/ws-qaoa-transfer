import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from circuit_generation import *
from calculations import *
from plotting import *
from graph_management import *


grid = np.load('./ws-energies/3reg1/3reg1_standard_energy.npy')
print(grid.shape)
g, b = maximizing_parameters(grid, plotting=False)
g, b = g[0], b[0]
print(g, b)
print(np.where(grid >= grid.max()-1e-5))
