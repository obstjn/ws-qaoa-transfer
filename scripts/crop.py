import os

input_dir = '/home/obstjn/Dokumente/MA/Latex/graphics/Deprecated/param_conc/'
output_dir = '/home/obstjn/Dokumente/MA/Latex/graphics/param_conc/'

for filename in os.listdir(input_dir):
  if filename.endswith('.pdf'):
    print(filename)
    os.system(f'pdfcrop {input_dir + filename} {output_dir + filename}')

