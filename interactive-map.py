import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt


from circuit_generation import *
from calculations import *
from plotting import *
from graph_management import *


ws_numbers_3reg0 = [0, 2, 8, 72, 74, 164, 62, 56, 18, 26, 20, 182]
ws_numbers_3reg1 = [0, 2, 60, 20, 78, 56, 6, 8, 24]
ws_numbers_3reg2 = [0, 6, 24, 8, 2]

ws_numbers_4reg0 = [0, 1, 3, 7, 24, 25, 27, 33, 35, 57, 23, 19, 17, 8, 15, 11, 9, 51, 41, 43]
ws_numbers_4reg1 = [0, 1, 3, 20, 21, 11, 8, 9, 28, 19, 17, 4, 7, 5, 25, 12, 13]
ws_numbers_4reg2 = [0, 1, 18, 13, 4, 5, 22, 17, 2, 3, 21, 6, 7]
ws_numbers_4reg3 = [0, 2, 6, 14, 1, 3]

ws_numbers_5reg0 = [0, 1, 3, 7, 15, 48, 49, 51, 55, 65, 67, 71, 113, 115, 195, 47, 39, 35, 33, 16, 31, 23, 19, 17, 103, 99, 81, 87, 83, 211]
ws_numbers_5reg1 = [0, 1, 3, 7, 40, 41, 43, 23, 16, 17, 19, 56, 57, 81, 39, 35, 33, 15, 11, 9, 51, 49, 24, 27, 25, 89]
ws_numbers_5reg2 = [0, 1, 3, 36, 37, 27, 8, 9, 11, 44, 45, 60, 35, 33, 7, 5, 43, 41, 12, 15, 13, 28]
ws_numbers_5reg3 = [0, 1, 34, 29, 4, 5, 28, 13, 12, 33, 3, 37, 6, 7, 14]
ws_numbers_5reg4 = [0, 2, 6, 14, 30, 1, 3, 7]

graph_data = []
for x in [3,4,5]:
  for i in range(x):
    graph_type = f'{x}reg{i}'
    for label, number in enumerate(eval(f'ws_numbers_{x}reg{i}')):
      # graph_type = 3reg0, number = ws-number, label = label as in thesis
      graph_data.append((graph_type, number, label))

gammaMax, betaMax = 2*np.pi, np.pi
map_data = np.load('./ws-energies/transferability/transferability_map.npy')
#map_data = np.load('./ws-energies/transferability/difference_map.npy')
_cmap = 'inferno'  # transferability: 'inferno'   difference: 'inferno_r'

fig = plt.figure('Interactive Map', figsize=(19.5, 12))


def format_landscape(ax):
  ax.set_xlabel(r'$\beta$')
  ax.set_ylabel(r'$\gamma$')
  ax.set_xticks(np.linspace(0, betaMax, 5))
  ax.set_yticks(np.linspace(0, gammaMax, 5))
  ax.xaxis.set_major_formatter(FormatStrFormatter('%.3g'))
  ax.yaxis.set_major_formatter(FormatStrFormatter('%.3g'))

# donor
ax_donor_graph = plt.axes([.05, .55, .1846, .3])
ax_donor_landscape = plt.axes([.26, .55, .1846, .3])
# format
format_landscape(ax_donor_landscape)
donor_landscape = ax_donor_landscape.imshow(np.ones((30,30)), cmap=_cmap, interpolation='none', origin='lower', extent=[0, betaMax, 0, gammaMax])
ax_donor_landscape.set_aspect(betaMax/gammaMax)

# acceptor
ax_acceptor_graph = plt.axes([.05, .15, .1846, .3])
ax_acceptor_landscape = plt.axes([.26, .15, .1846, .3])
# format
format_landscape(ax_acceptor_landscape)
acceptor_landscape = ax_acceptor_landscape.imshow(np.ones((30,30)), cmap=_cmap, interpolation='none', origin='lower', extent=[0, betaMax, 0, gammaMax])
ax_acceptor_landscape.set_aspect(betaMax/gammaMax)

# plot map
ax_map = plt.axes([.5, .05, .5, .9])
ax_map.set_xlabel('Donor subgraph', fontsize='x-large')
ax_map.set_ylabel('Acceptor subgraph', fontsize='x-large')
map_text = ax_map.text(0.76, -0.03, '', fontsize=16, transform=ax_map.transAxes)
img = ax_map.imshow(map_data, cmap=_cmap, interpolation='none')
plt.colorbar(img)

# line seperators
location = -0.5  # seperator between pixels
ticks = []
labels = []
for x in [3, 4, 5]:
  for i in range(x):
    numbers = eval(f'ws_numbers_{x}reg{i}')
    location += len(numbers)
    if location < 180:  # skip last lines
      ax_map.axvline(x=location, color='white', linestyle='--')
      ax_map.axhline(y=location, color='white', linestyle='--')

    ticks.append(location - len(numbers)/2)
    labels.append(f'{x}reg{i}')
    
# map labels
plt.xticks(ticks, labels)
plt.yticks(ticks, labels)
ax_map.xaxis.tick_top()
ax_map.set_title('Transferability coefficients', fontsize='30', y=1.05)
ax_donor_landscape.set_title('Donor landscape')
ax_acceptor_landscape.set_title('Acceptor landscape')


def draw_graph(G, warmstarting, axes):
  apx_sol = np.array(warmstarting)
  attrs = {i: apx_sol[i] for i in range(len(apx_sol))}
  nx.set_node_attributes(G, attrs, name='weight')

  # plotting
  cmap = {0: '#6b00c2', 1: '#ffd500'}
  colors = [cmap[G.nodes[n]['weight']] for n in G.nodes]
  nx.draw_kamada_kawai(G, node_color=colors, ax=axes)


def update_step(graph_type, num, landscape, graph_ax):
  # landscape
  energy = np.load(f'./ws-energies/{graph_type}/energies/{num}_energy.npy')
  landscape.set_data(energy)
  landscape.autoscale()

  # graph
  G = nx.read_adjlist(f'./graphs/{graph_type}.graph', nodetype=int)
  base=2
  if graph_type[0] == '3': 
    base=3 
  ws = number_to_ws(num, len(G), base)
  draw_graph(G, ws, graph_ax)


def update(event):
  active_tool = fig.canvas.manager.toolbar.mode 
  if event.inaxes != ax_map or active_tool != '':
      return

  x, y = int(event.xdata + .5), int(event.ydata + .5)
  map_text.set_text(f'coefficient: {map_data[x,y]:.4f}')
  acc_type, acc_num, acc_label = graph_data[x]
  don_type, don_num, don_label = graph_data[y]

  # update donor
  ax_donor_graph.clear()
  ax_donor_graph.set_title('Donor graph')
  ax_donor_graph.text(0.76, 1.02, f'{don_type}  ({don_label})', transform=ax_donor_graph.transAxes)
  update_step(don_type, don_num, donor_landscape, ax_donor_graph)

  # update acceptor
  ax_acceptor_graph.clear()
  ax_acceptor_graph.set_title('Acceptor graph')
  ax_acceptor_graph.text(0.76, 1.02, f'{acc_type}  ({acc_label})', transform=ax_acceptor_graph.transAxes)
  update_step(acc_type, acc_num, acceptor_landscape, ax_acceptor_graph)

  # draw
  fig.canvas.draw()

fig.canvas.mpl_connect('button_press_event', update)
plt.show()
