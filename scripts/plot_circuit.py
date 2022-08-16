import matplotlib.pyplot as plt
import networkx as nx
from circuit_generation import qaoa_circuit


G = nx.read_adjlist('./graphs/3reg1.graph', nodetype=int)

qc = qaoa_circuit(G)#, apx_sol=[1,0,0,1,0])

hdata = [d for d in qc.data if d[0].name == 'h']
costdata = [d for d in qc.data if d[0].name == 'rzz']
mixerdata = [d for d in qc.data if d[0].name == 'rx']
qc.data = hdata
qc.barrier()
qc.data += costdata
qc.barrier()
qc.data += mixerdata

#qc.draw('mpl')#, filename='G3reg1_qc.png')

