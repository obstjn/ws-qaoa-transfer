from plotting import *
from calculations import *


energy_grids = sorted(os.listdir('./energies/ordered'))

numbers = (228, 232, 479)
numbers = list(map(str, numbers))
f = lambda x: x[:3] in numbers
files = filter(f, energy_grids)


draw_multiple_landscapes_and_graphs([f'energies/ordered/{file}' for file in files], rows=1, cols=3, figsize=(7.166, 7.166*0.4))
plt.savefig('random_equivalence.pdf')
plt.show()