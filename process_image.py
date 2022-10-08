import os
import glob
from random import shuffle
import numpy as np


def hcombine_images(list_images, name):
    from PIL import Image
    imgs = [Image.open(i) for i in list_images]
    # pick the image which is the smallest, and resize the others to match it
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))

    # save that beautiful picture
    imgs_comb = Image.fromarray(imgs_comb)
    imgs_comb.save(name + '.png')


def vcombine_images(list_images, path, name):
    from PIL import Image
    import pandas as pd
    import random

    level = [os.path.basename(i)[-6:-4] for i in list_images]
    shuffled_images = list(enumerate(list_images))
    random.shuffle(shuffled_images)
    idx, list_images = zip(*shuffled_images)
    idx = [os.path.basename(i)[-5:-4] for i in list_images]
    my_dict = {"level": level, "row": idx}
    df = pd.DataFrame.from_dict(my_dict)
    df.to_csv(path + "/" + name + '-map.csv', index=False, header=True)

    imgs = [Image.open(i) for i in list_images]
    # pick the image which is the smallest, and resize the others to match it
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))

    # save that beautiful picture
    imgs_comb = Image.fromarray(imgs_comb)
    imgs_comb.save(path + "/" + name + '.png')


src_path = os.getcwd()                  # getting my current path
images_dir_path = src_path + '/images'  # selecting images folder

# selecting directories in images folder
directories = glob.glob(os.path.join(images_dir_path, '*'))

# removing png and csv files
removing_files = glob.glob(os.path.join(images_dir_path, '*.png'))
extra = glob.glob(os.path.join(images_dir_path, '*.csv'))
removing_files += extra
for i in removing_files:
    os.remove(i)

for directory in directories:
    removing_files = glob.glob(os.path.join(directory, '*.png'))
    extra = glob.glob(os.path.join(directory, '*.csv'))
    removing_files += extra
    for i in removing_files:
        os.remove(i)


for directory in directories:

    level_dir = glob.glob(os.path.join(directory, '*'))  # list of levels
    for level in level_dir:
        # list of images in current level
        list_im = glob.glob(os.path.join(level, '*'))
        hcombine_images(list_im, level)  # combining horizontally the images

    # now that images are combined horizontally (same level)
    # we combine then vertically (different level)
    # in particular we put for each row a level
    # notice that this is done randomically!
    # we provide csv file with conversion row level
    list_im = glob.glob(os.path.join(directory, '*.png'))
    name = os.path.basename(directory)
    vcombine_images(list_im, src_path, name)
    # removing images
    for i in list_im:
        os.remove(i)
