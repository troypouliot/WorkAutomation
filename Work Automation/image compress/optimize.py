from PIL import Image
from time import sleep
from os import listdir, getcwd, mkdir
from os.path import join, splitext, exists

source_dir = getcwd()

# source_dir = abspath(r'D:\My Drive\Business\Website\Pages\Product Gallery')

output_dir = join(source_dir, 'Optimized')

if not exists(output_dir):
    print(output_dir + ' Does not exist. Creating...')
    mkdir(output_dir)

max_size = (1000, 1000)

images = [file for file in listdir(source_dir) if file.endswith('jpg')]

for image in images:
    # 1. Open the image
    img = Image.open(join(source_dir, image))
    # 2. Resize the image
    img.thumbnail(max_size, Image.ANTIALIAS)
    # 3. Compressing the image
    img.save(join(output_dir, splitext(image)[0] + '_opt' + ".jpg"),
             optimize=True,
             quality=65)
    sleep(1)
