import numpy as np
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

from calculations import *
from circuit_generation import *
from plotting import *
from graph_management import *


def special_get_energy_grid(G, qaoa_qc, edge, gammaMax=2*np.pi, betaMax=np.pi, betaMin=0, samples=100):
  """  Calculate the energies for a 2D parameter space.  """
  gammas, betas = np.mgrid[0:gammaMax:gammaMax/samples, betaMin:betaMax:(betaMax-betaMin)/samples]
  result = np.empty((samples,samples))

  print('Calculating energy:')
  for i in range(samples):
    for j in range(samples):
      result[i,j] = get_energy(G, qaoa_qc, gammas[i,j], betas[i,j], edge)

      # progress bar
      bar_len = 60
      progress = int(bar_len*(i*samples + j)/(samples**2)) + 1
      print('\r{0}{1}'.format('\u2588' * progress, '\u2591' * (bar_len-progress)), end='')
      print('\t' + f'{(i*samples + j + 1)}/{samples**2} samples', end='')
  print()
  return result


def special_plot_energy(energy_grid, gammaMax=2*np.pi, betaMax=np.pi, betaMin=0, title=None, filename=None, show=True):
  fig, ax = plt.subplots()
  ax.set_title(title)
  img = ax.imshow(energy_grid, cmap='inferno', origin='lower', extent=[betaMin, betaMax, 0, gammaMax])
  plt.colorbar(img)

  ax.set_aspect(0.5)
  ax.set_xlabel(r'$\beta$')
  ax.set_ylabel(r'$\gamma$')
  plt.xticks(np.arange(betaMin, betaMax, 0.25*np.pi))
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


# calculate energy grid for bigger beta values
#Grand = nx.fast_gnp_random_graph(8, .25, seed=3)
#samples = 64
#bMin, bMax = -0.25*np.pi, 4.2
#subgraphs = get_subgraphs(Grand)
#grid = np.zeros((samples,samples))
#
#for item in subgraphs:
#  subgraph, edge, occurrence = item
#  qc = qaoa_circuit(subgraph)
#
#  grid += special_get_energy_grid(subgraph, qc, edge, betaMax=bMax, betaMin=bMin, samples=samples) * occurrence
#
#np.save('random-graph-special-energy.npy', grid)
#special_plot_energy(grid, betaMax=bMax, betaMin=bMin)
