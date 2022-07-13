import os

input_dir = '/home/obstjn/Dokumente/MA/code/ws-energies/plots/energy-plots/5reg3/'
output_dir = '/home/obstjn/Dokumente/MA/Latex/graphics/regular_ws_landscapes/'

for filename in os.listdir(input_dir):
  if filename.endswith('.pdf'):
    print(filename)
    os.system(f'pdfcrop {input_dir + filename} {output_dir + filename}')

