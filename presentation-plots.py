import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from circuit_generation import *
from calculations import *
from plotting import *
from graph_management import *


G = nx.read_adjlist('./graphs/3reg1.graph', nodetype=int)
apx_sol = np.array([1, 0, 0, 1, 0])
#draw_graph_with_ws(G, apx_sol, show=False)
draw_graph_with_cut(G, apx_sol, draw_labels=True, show=False)
qc = qaoa_circuit(G, apx_sol)
qc.draw('mpl')
plt.show()
