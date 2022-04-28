import numpy as np
import matplotlib.pyplot as plt
import os

from matplotlib.ticker import FormatStrFormatter

def plot_energy(energy_grid, gammaMax=2*np.pi, betaMax=np.pi, title=None, filename=None):
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
    plt.savefig(f'{filename}_energy-landscape.png', dpi=300)
  else:
    plt.show()


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
