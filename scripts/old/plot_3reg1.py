import numpy as np
from itertools import product
import matplotlib.pyplot as plt
from plotting import plot_energy_with_marker

done = []
idx = []
skip = [17, 41, 112, 121, 130, 201, 225]
n = 0
for i, x in enumerate(product([0, .5, 1], repeat=5)):
    x = np.array(x)
    if str(x) in done or i in skip:
        continue

    energy_grid = np.load(f'./ws-energies/3-reg_1/energies/{i}_energy.npy')

    # remove duplicates
    pattern_set = list({str(x[::-1]), str(x), str(np.abs(x-1)), str(np.abs(x-1)[::-1])})
    done.extend(pattern_set)
    idx.append(i)

    len_p = len(pattern_set)
    if len_p ==1:
        ws_conf = pattern_set[0]
    elif len_p == 2:
        ws_conf = pattern_set[0] + '  ' + pattern_set[1]
    elif len_p == 4:
        ws_conf = pattern_set[0] + '  ' + pattern_set[1] + '\n' + pattern_set[2] + '  ' + pattern_set[3]


    #plot_energy_with_marker(energy_grid, marker='max', title=ws_conf, filename=f'./ws-energies/3-reg_1/plots/temp/{i}')
    
# check for duplicates
for i in range(len(idx)):
    e1 = np.load(f'./ws-energies/3-reg_1/energies/{idx[i]}_energy.npy')
    for j in range(i+1, len(idx)):
        e2 = np.load(f'./ws-energies/3-reg_1/energies/{idx[j]}_energy.npy')
        if np.allclose(e1, e2):
            print(idx[i], idx[j])
