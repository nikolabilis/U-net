from __future__ import print_function
from keras.utils.np_utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
import glob
import skimage.io as io
import skimage.transform as trans
from PIL import Image

Sky = [128, 128, 128]
Building = [128, 0, 0]
Pole = [192, 192, 128]
Road = [128, 64, 128]
Pavement = [60, 40, 222]
Tree = [128, 128, 0]
SignSymbol = [192, 128, 128]
Fence = [64, 64, 128]
Car = [64, 0, 128]
Pedestrian = [64, 64, 0]
Bicyclist = [0, 128, 192]
Unlabelled = [0, 0, 0]
prva = [0, 0, 0]
druga = [60, 60, 60]
treca = [120, 120, 120]
cetvrta = [180, 180, 180]
peta = [240, 240, 240]

COLOR_DICT = np.array([prva, druga, treca, cetvrta, peta])


def adjustData(img, mask, flag_multi_class, num_class):
    img = img / 255
    for k in range(np.shape(mask)[0]):
        for i in range(np.shape(mask)[1]):
            for j in range(np.shape(mask)[2]):
                if mask[k, i, j] == 60:
                    mask[k, i, j] = 1
                elif mask[k, i, j] == 120:
                    mask[k, i, j] = 2
                elif mask[k, i, j] == 180:
                    mask[k, i, j] = 3
                elif mask[k, i, j] == 240:
                    mask[k, i, j] = 4
                else:
                    mask[k, i, j] = 0

    mask = np.reshape(mask, (mask.shape[0], mask.shape[1], mask.shape[2], 1))
    mask = to_categorical(mask, num_classes=5)
    img = np.reshape(img, (img.shape[0], img.shape[1], img.shape[2], 1))

    return (img, mask)


def trainGenerator(batch_size, train_path, image_folder, mask_folder, aug_dict, image_color_mode="grayscale",
                   mask_color_mode="grayscale", image_save_prefix="image", mask_save_prefix="mask",
                   flag_multi_class=False, num_class=5, save_to_dir=None, target_size=(256, 256), seed=1):
    '''
    can generate image and mask at the same time
    use the same seed for image_datagen ahttps://github.com/keras-team/keras-preprocessing/issues/125nd mask_datagen to ensure the transformation for image and mask is the same
    if you want to visualize the results of generator, set save_to_dir = "your path"
    '''
    image_datagen = ImageDataGenerator(**aug_dict)
    mask_datagen = ImageDataGenerator(**aug_dict)
    image_generator = image_datagen.flow_from_directory(
        train_path,
        classes=[image_folder],
        class_mode=None,
        color_mode=image_color_mode,
        target_size=target_size,
        batch_size=batch_size,
        save_to_dir=save_to_dir,
        save_prefix=image_save_prefix,
        seed=seed)
    mask_generator = mask_datagen.flow_from_directory(
        train_path,
        classes=[mask_folder],
        class_mode=None,
        color_mode=mask_color_mode,
        target_size=target_size,
        batch_size=batch_size,
        save_to_dir=save_to_dir,
        save_prefix=mask_save_prefix,
        seed=seed)
    train_generator = zip(image_generator, mask_generator)
    for (img, mask) in train_generator:
        img, mask = adjustData(img, mask, flag_multi_class, num_class)
        yield (img, mask)


def testGenerator(test_path, num_image=30, target_size=(256, 256, 1), flag_multi_class=False, as_gray=True):
    for i in range(num_image):
        img = io.imread(os.path.join(test_path, "%d.tif" % i), as_gray=as_gray)
        img = img / 255
        img = trans.resize(img, target_size)
        img = np.reshape(img, img.shape + (1,)) if (not flag_multi_class) else img
        img = np.reshape(img, (1,) + img.shape)
        yield img


def geneTrainNpy(image_path, mask_path, flag_multi_class=True, num_class=5, image_prefix="image", mask_prefix="mask",
                 image_as_gray=True, mask_as_gray=True):
    image_name_arr = glob.glob(os.path.join(image_path, "%s*.png" % image_prefix))
    image_arr = []
    mask_arr = []
    for index, item in enumerate(image_name_arr):
        img = io.imread(item, as_gray=image_as_gray)
        img = np.reshape(img, img.shape + (1,)) if image_as_gray else img
        mask = io.imread(item.replace(image_path, mask_path).replace(image_prefix, mask_prefix), as_gray=mask_as_gray)
        mask = np.reshape(mask, mask.shape + (1,)) if mask_as_gray else mask
        img, mask = adjustData(img, mask, flag_multi_class, num_class)
        image_arr.append(img)
        mask_arr.append(mask)
    image_arr = np.array(image_arr)
    mask_arr = np.array(mask_arr)
    return image_arr, mask_arr


def labelVisualize(img):
    img_out = np.zeros([img.shape[0], img.shape[1]])
    for i in range(np.shape(img)[0]):
        for j in range(np.shape(img)[1]):
            max = 0
            for k in range(np.shape(img)[2]):
                if img[i, j, k] > max:
                    max = img[i, j, k]
                    img_out[i, j] = k * 60
    return img_out


def saveResult(save_path, npyfile):
    for i, item in enumerate(npyfile):
        img = labelVisualize(item)
        io.imsave(os.path.join(save_path, "%d.png" % i), img / 240)
