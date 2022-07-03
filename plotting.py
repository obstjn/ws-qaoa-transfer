import numpy as np
import matplotlib.pyplot as plt
import os
import networkx as nx

from matplotlib.ticker import FormatStrFormatter

def plot_energy(energy_grid, gammaMax=2*np.pi, betaMax=np.pi, title=None, filename=None, show=True):
  fig, ax = plt.subplots()
  ax.set_title(title)
  img = ax.imshow(energy_grid, cmap='inferno', origin='lower', extent=[0, betaMax, 0, gammaMax])
  plt.colorbar(img)

  ax.set_aspect(betaMax/gammaMax)
  ax.set_xlabel(r'$\beta$')
  ax.set_ylabel(r'$\gamma$')
  plt.xticks(np.linspace(0, betaMax, 5))
  plt.yticks(np.linspace(0, gammaMax, 5))
  ax.xaxis.set_major_formatter(FormatStrFormatter('%.3g'))
  ax.yaxis.set_major_formatter(FormatStrFormatter('%.3g'))
  if filename is not None:
    plt.savefig(f'{filename}_energy-landscape.pdf')#, dpi=300)
    plt.close()
  else:
    if show:
        plt.show()
    else:
        pass


def plot_energy_with_marker(energy_grid, gammaMax=2*np.pi, betaMax=np.pi, marker='max', title=None, filename=None, show=True, a=1.0):
  thresh= a*energy_grid.max() + (1-a)*energy_grid.min() - 1e-5
  if marker == 'max':
    gam_idx, bet_idx = np.where((energy_grid >= thresh)) 
  elif marker == 'min':
    gam_idx, bet_idx = np.where((energy_grid <= energy_grid.max()+1e-5)) 
  else:
    gam_idx, bet_idx = np.where((energy_grid >= energy_grid.max()-1e-5) | (energy_grid <= energy_grid.min()+1e-5))

  gam = gam_idx + .5  # add half a pixel
  bet = bet_idx + .5
  gam *= 2*np.pi/energy_grid.shape[0]  # adjust scale
  bet *= 1*np.pi/energy_grid.shape[1]

  fig, ax = plt.subplots()
  ax.set_title(title)
  vmin, vmax = .18, .94
  vmin, vmax = None, None  # relative color scale
  img = ax.imshow(energy_grid, cmap='inferno', vmin=vmin, vmax=vmax, origin='lower', extent=[0, betaMax, 0, gammaMax])
  plt.colorbar(img)
  plt.scatter(bet, gam, s=120, linewidths=2.0, facecolors='none', color='deepskyblue')
  
  # temp delete
  #a= .8
  #thresh= a*energy_grid.max() + (1-a)*energy_grid.min() - 1e-5
  #gam_idx, bet_idx = np.where((energy_grid >= thresh)) 
  #gam = gam_idx + .5  # add half a pixel
  #bet = bet_idx + .5
  #gam *= 2*np.pi/energy_grid.shape[0]  # adjust scale
  #bet *= 1*np.pi/energy_grid.shape[1]
  #plt.scatter(bet, gam, s=120, linewidths=2.0, facecolors='none', color='red')
  ######

  ax.set_aspect(betaMax/gammaMax)
  ax.set_xlabel(r'$\beta$')
  ax.set_ylabel(r'$\gamma$')
  plt.xticks(np.linspace(0, betaMax, 5))
  plt.yticks(np.linspace(0, gammaMax, 5))
  ax.xaxis.set_major_formatter(FormatStrFormatter('%.3g'))
  ax.yaxis.set_major_formatter(FormatStrFormatter('%.3g'))
  if filename is not None:
    plt.savefig(f'{filename}_energy-landscape.pdf')#, dpi=300)
    plt.close()
  else:
    if show:
        plt.show()
    else:
        pass


def save_contents(G, qaoa_qc, energy_grid, name, hyperparams=None, folder=None):
  save = input(f'save to /{folder}/{name}? previous data is overwritten! y/n\n')
  if save != 'y':
    return
  #drive_path = '/content/drive/MyDrive/MA/'
  drive_path = './'
  if folder is not None:
    os.makedirs(drive_path + folder, exist_ok=True)
    path = drive_path + f'{folder}/{name}'
  else:
    path = drive_path + name
  nx.write_weighted_edgelist(G, f'{path}.graph')
  nx.draw(G, with_labels=False)
  plt.savefig(f'{path}_graph.png', dpi=150)
  transpile(qaoa_qc, basis_gates=['h', 'rz', 'rx', 'cx']).draw('mpl', filename=f'{path}_qaoa.png')
  np.save(f'{path}_energy.npy', energy_grid)
  plot_energy(energy_grid, filename=path)


""" 3D-Plot """
def plot_3d():
  samples = 65
  gammas, betas = np.mgrid[0:2*np.pi:samples*1j, 0:np.pi:samples*1j]
  fig, ax = plt.subplots(dpi=150, subplot_kw={"projection": "3d"})
  ax.view_init(elev=30, azim=30)
  surf = ax.plot_surface(gammas, betas, energy_grid, cmap='inferno',
                         linewidth=0, antialiased=False)
  plt.show()


""" graph drawing """
def node_color_mapping(G, cut):
  """ returns a color mapping where the nodes are colored by partition."""
  cut = cut[::-1]
  color_map =[]
  for x in range(len(G)):
    if cut[x] == '1' or cut[x] == 1:
      color_map.append('red')
    else:
      color_map.append('#1f78b4')  # default networkx color
  return color_map


def edge_color_mapping(G, cut):
  """ returns a color mapping where edges belonging to the cut are highlighted."""
  edges = G.edges()
  cut = cut[::-1]  # reverse cut
  edge_color = []
  for u, v in edges:
    if cut[u] != cut[v]:
      edge_color.append('darkorange')
    else:
      edge_color.append('k')  # default networkx edge color
  return edge_color


def draw_graph_with_cut(G, cut, draw_labels=False, show=True):
  edge_colors = edge_color_mapping(G, cut)
  node_colors = node_color_mapping(G, cut)
  plt.figure()
  nx.draw_kamada_kawai(G, node_color=node_colors, edge_color=edge_colors, width=1.4, with_labels=draw_labels)
  if show: plt.show()


def draw_graph_with_ws(G, warmstarting=None, show=True):
  if warmstarting is not None:
    if len(warmstarting) != len(G):
      raise ValueError('Invalid warmstarting for the given graph!')
    apx_sol = np.array(warmstarting)
    attrs = {i: apx_sol[i] for i in range(len(apx_sol))}
    nx.set_node_attributes(G, attrs, name='weight')

  # plotting
  cmap = {0.: '#6b00c2', .5: '#1f78b4', 1.: '#ffd500'}
  colors = [cmap[G.nodes[n]['weight']] for n in G.nodes]
  plt.figure()
  nx.draw_kamada_kawai(G, with_labels=True, node_color=colors, font_color='k')
  if show:
    plt.show()
  else:
    pass

