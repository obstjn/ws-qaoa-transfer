import numpy as np

X = 5
opt_values = np.load(f'./{X}reg/opt_values.npy')
opt_energies = np.load(f'./{X}reg/opt_energies.npy')
rand_energies = np.load(f'./{X}reg/rand_energies.npy')
deopt_energies = np.load(f'./{X}reg/deopt_energies.npy')

print(f'average deoptimized energy: {np.average(deopt_energies/opt_values)}\tstd: {np.std(deopt_energies/opt_values)}')
print(f'average random energy:      {np.average(rand_energies/opt_values)}\tstd: {np.std(rand_energies/opt_values)}')
print(f'average optimized energy:   {np.average(opt_energies/opt_values)}\tstd: {np.std(opt_energies/opt_values)}')
