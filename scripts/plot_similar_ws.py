import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from plotting import *

import os
from itertools import product


# 3-regular graphs
G_3reg0 = Graph()
G_3reg1 = Graph()
G_3reg2 = Graph()
G_3reg0.add_edges_from([(0,2), (1,2), (2,3), (3,4), (3,5)]) 
G_3reg1.add_edges_from([(0,1), (1,2), (1,3), (2,3), (3,4)])
G_3reg2.add_edges_from([(0,1), (0,2), (0,3), (1,3), (2,3)])

e_3reg0 = (2,3)
e_3reg1 = (1,3)
e_3reg2 = (0,3)

list_3reg = [(G_3reg0, e_3reg0), (G_3reg1, e_3reg1), (G_3reg2, e_3reg2)]

# map reg0 --> reg1: 0,4 --> 2
#                    0 --> 0, 5 --> 4
# reg0 --> reg2: 0,4 --> 1
#                1,5 --> 2
# reg1 --> reg2: 0,4 --> 1
# take little ws (e.g. reg2 and "split" node (create new ws)


# analogous ws 3reg2 --> 3reg1
#folder2 = f'./ws-energies/3reg2/energies/'
#folder1 = f'./ws-energies/3reg1/energies/'
#
#for filename in sorted(os.listdir(folder2)):
#    k2 = int(filename.split('_')[0])
#    ws2 = number_to_ws(k2, 4)  # ws for G_3reg2
#
#    # create analogous ws
#    ws1 = np.empty(5)
#    ws1[0] = ws2[1]
#    ws1[1] = ws2[0]
#    ws1[2] = ws2[2]
#    ws1[3] = ws2[3]
#    ws1[4] = ws2[1]
#    k1 = int(sum([n * 2 * 3**i for i,n in enumerate(ws1)]))
#    
#    e2 = np.load(folder2 + filename)
#    try:
#        e1 = np.load(folder1 + f'{k1}_energy.npy')
#        plot_energy(e2, title=str(ws2), show=False)
#        plot_energy(e1, title=str(ws1), show=False)
#        plt.show()
#    except:
#        k1a = int(sum([n * 2 * 3**i for i,n in enumerate(np.abs(ws1-1))]))
#        k1b = int(sum([n * 2 * 3**i for i,n in enumerate(np.abs(ws1-1)[::-1])]))
#        if k1a < k1b:
#            k1 = k1a
#            ws1 = np.abs(ws1-1)
#        else:
#            k1 = k1b
#            ws1 = np.abs(ws1-1)[::-1]
#
#        e1 = np.load(folder1 + f'{k1}_energy.npy')
#        plot_energy(e2, title=str(ws2), show=False)
#        plot_energy(e1, title=str(ws1), show=False)
#        plt.show()


folder1 = f'./ws-energies/3reg1/energies/'
folder0 = f'./ws-energies/3reg0/energies/'

for filename in sorted(os.listdir(folder1)):
    k1 = int(filename.split('_')[0])
    ws1 = number_to_ws(k1, 5)  # ws for G_3reg1

    # create analogous ws
    ws0 = np.empty(6)
    ws0[0] = ws1[0]
    ws0[1] = ws1[2]
    ws0[2] = ws1[1]
    ws0[3] = ws1[3]
    ws0[4] = ws1[2]
    ws0[5] = ws1[4]
    k0 = int(sum([n * 2 * 3**i for i,n in enumerate(ws0)]))
    
    e1 = np.load(folder1 + filename)
    try:
        e0 = np.load(folder0 + f'{k0}_energy.npy')
        plot_energy(e1, title=str(ws1), show=False)
        plot_energy(e0, title=str(ws0), show=False)
        plt.show()
    except:
        continue
        k0a = int(sum([n * 2 * 3**i for i,n in enumerate(np.abs(ws0-1))]))
        k0b = int(sum([n * 2 * 3**i for i,n in enumerate(np.abs(ws0-1)[::-1])]))
        if k0a < k0b:
            k0 = k0a
            ws0 = np.abs(ws0-1)
        else:
            k0 = k0b
            ws0 = np.abs(ws0-1)[::-1]

        e0 = np.load(folder0 + f'{k0}_energy.npy')
        plot_energy(e1, title=str(ws1), show=False)
        plot_energy(e0, title=str(ws0), show=False)
        plt.show()



