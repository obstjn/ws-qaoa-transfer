import numpy as np
from calculations import *
from plotting import *
import matplotlib.pyplot as plt
import os


assigned = []
nn = 0

folder = './ws-energies/3reg2/energies/'

# take all files of folder
for filename in sorted(os.listdir(folder)):
  # number of grid
  k = int(filename.split('_')[0])

  # k already in a group
  if k in assigned:
    continue

  e1 = np.load(folder + filename)
  # group of transferable
  transferable = [k]
  assigned.append(k)
  
  for filename in sorted(os.listdir(folder)):
    l = int(filename.split('_')[0])

    if k == l or l in assigned:
      continue

    e2 = np.load(folder + filename)
    if param_transferable(e1, e2) and param_transferable(e2, e1):
      assigned.append(l)
      transferable.append(l)

  print(transferable)
  for i in transferable:
    e = np.load(folder + f'{i}_energy.npy')
    plot_energy_with_marker(e, title=number_to_ws(i, 4), a=.7)
  plt.show()

#for i in [100, 11, 14, 18, 19, 20]:
#  e = np.load(folder + f'{i}_energy.npy')
#  e14 = np.load(folder + f'{14}_energy.npy')
#  print(param_transferable(e14, e), param_transferable(e, e14))
#  plot_energy_with_marker(e, a=.7)
#plt.show()
