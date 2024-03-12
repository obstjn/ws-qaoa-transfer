from plotting import *
from calculations import *


# G, ws, grid_a = get_graph_ws_and_grid('./energies/ordered/094_(2-5)-0-0010011.npy')
# draw_landscape_and_graph(grid_a, G, ws, show=False, title='94')
# G, ws, grid_b = get_graph_ws_and_grid('./energies/ordered/167_(3-4)-0-1001001.npy')
# draw_landscape_and_graph(grid_b, G, ws, show=False, title='167')

# print(transferability_coeff(grid_b, grid_a))
# print(transferability_coeff(grid_a, grid_b))
# plt.show()


files = ['345_(4-5)-0-000110001.npy',
'346_(4-5)-0-000110011.npy',
'347_(4-5)-0-000110111.npy',
'348_(4-5)-0-000111111.npy',
'349_(4-5)-0-001110000.npy',
'350_(4-5)-0-001110001.npy',
'351_(4-5)-0-001110011.npy',
'352_(4-5)-0-001110111.npy',
'353_(4-5)-0-001111111.npy',
'354_(4-5)-0-100001111.npy',
'355_(4-5)-0-100000111.npy',
'356_(4-5)-0-100000011.npy',
'357_(4-5)-0-100000001.npy',
'358_(4-5)-0-100000000.npy',
'359_(4-5)-0-100011111.npy',
'360_(4-5)-0-100010111.npy',
'361_(4-5)-0-100010011.npy',
'362_(4-5)-0-100010001.npy',
'149_(3-4)-0-0000000.npy',
'150_(3-4)-0-0000001.npy',
'151_(3-4)-0-0000011.npy',
'152_(3-4)-0-0000111.npy',
'153_(3-4)-0-0001000.npy',
'154_(3-4)-0-0001001.npy',
'155_(3-4)-0-0001011.npy',
'156_(3-4)-0-0001111.npy',
'157_(3-4)-0-0011000.npy',
'158_(3-4)-0-0011001.npy',
'159_(3-4)-0-0011011.npy',
'160_(3-4)-0-0011111.npy']

print(len(files))
draw_multiple_landscapes_and_graphs([f'energies/ordered/{file}' for file in files], rows=5, cols=6)
plt.show()