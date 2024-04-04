# generate the matrix for the latex figures

import os


rows = ['q', 'r', 'x', 'y', 'z']
cols = ['a', 'b', 'c', 'd', 'e', 'f']

numbers = []
input_dir = '/home/obstjn/Dokumente/MA/code/ws-energies/5reg3/energies/'
for filename in os.listdir(input_dir):
  numbers.append(int(filename.split('_')[0]))
numbers = sorted(numbers)

left = [0, 1, '', '', '', 34, 29, '', '', 4, 5, '', 28, 13, 12]
right = ['', '', '', 33, '', '', '', '', 3, '', 37, 6, '', 7, 14]
numbers = []

while left:
  numbers.extend(left[:3] + right[:3][::-1])
  left = left[3:]
  right = right[3:]

i = 0 
for r in rows:
  for c in cols:
    if i < len(numbers):
      print(f'\\def\\{r}{c}' + '{' + str(numbers[i]) + '}\t', end='')
    else:
      print(f'\\def\\{r}{c}' + '{0}\t', end='')
    i += 1
  print()

