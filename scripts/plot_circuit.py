import matplotlib.pyplot as plt
from networkx import Graph
from circuit_generation import qaoa_circuit


G = Graph()
G.add_edges_from([(0,1), (1,2), (1,3), (2,3), (3,4)])

qc = qaoa_circuit(G, apx_sol=[1,1,0,0,0])

qc.draw('mpl', filename='3reg1_ws_circuit.pdf')
