import numpy as np

mini, maxi = 1, 0

for i in range(3**5):
    path = f"../ws-energies/3-reg_2/energies/{i}_energy.npy"
    energy_grid = np.load(path)
    mini = min(mini, energy_grid.min())
    maxi = max(maxi, energy_grid.max())
    
print(mini, maxi)
