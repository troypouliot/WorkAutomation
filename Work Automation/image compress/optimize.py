from PIL import Image
from time import sleep
from os import listdir, getcwd, mkdir
from os.path import join, splitext, exists

source_dir = getcwd()

# source_dir = abspath(r'D:\My Drive\Business\Website\Pages\Product Gallery')

output_dir = join(source_dir, 'Optimized')
max_size = ''

try:
    print('Enter the max width/height in px (enter like so "800,600")')
    max_size = (input('Enter q to quit.')).lower().split(',')
    if max_size[0] == 'q':
        exit()
    else:
        max_size = (int(max_size[0]), int(max_size[1]))
except (ValueError, IndexError):
    print('Try again, make sure you use the format width,height')
    max_size = (input('Enter q to quit.')).lower().split(',')
    if max_size[0] == 'q':
        exit()
    else:
        max_size = (int(max_size[0]), int(max_size[1]))


if not exists(output_dir):
    print(output_dir + ' Does not exist. Creating...')
    mkdir(output_dir)



images = [file for file in listdir(source_dir) if file.endswith('jpg')]

for image in images:
    # 1. Open the image
    print('Optimizing:  {}'.format(image))
    img = Image.open(join(source_dir, image))
    # 2. Resize the image
    img.thumbnail(max_size, Image.ANTIALIAS)
    # 3. Compressing the image
    img.save(join(output_dir, splitext(image)[0] + '_opt' + ".jpg"),
             optimize=True,
             quality=65)
    print('{}  is done'.format(image))
    sleep(1)
print('All done, Goodbye')
sleep(2)
