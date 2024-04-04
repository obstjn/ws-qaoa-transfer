from itertools import product
import numpy as np


[0]
[1, 81]
[2, 80]
[3, 27]
[4, 108]
[5, 53]
[6, 54]
[7, 107]
[8, 17, 26]
[9]
[10, 90]

def array_to_num(arr):
    number = 0
    for j,n in enumerate(np.array(arr)*2):
        number += n * 3**j


#for i, x in enumerate(product([1, .5, 0], repeat=5)):
#    number = 0
#    inverted = x[::-1]
#    inverse = np.abs(np.array(x)-1)
#    inverse_inv = inverse[::-1]
#    
#    for j,n in enumerate(np.array(x)*2):
#        number += n * 3**j
#
#    number = int(number)
#    print(i, x, inverse, inverted, inverse_inv)


for i, x in enumerate(product([0, .5, 1], repeat=5)):
    print(i, x[::-1])
