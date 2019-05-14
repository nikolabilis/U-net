

from PIL import Image





def red(pixel):
    return pixel[0] > 250 and pixel[1] < 5 and pixel[2] < 5 and pixel[3] > 250
def yellow(pixel):
    return pixel[0] > 250 and pixel[1] > 250 and pixel[2] < 5 and pixel[3] > 250
def green(pixel):
    return pixel[0] < 5 and pixel[1] > 250 and pixel[2] < 5 and pixel[3] > 250
def blue(pixel):
    return pixel[0] < 5 and pixel[1] < 5 and pixel[2] > 250 and pixel[3] > 250


def find_borders(width_pixel, pixels, prev_pixel_loc, image):
    pixel_loc = []
    width = image.size[0]
    height = image.size[1]
    area = 70

    x = prev_pixel_loc[0] - area
    y = prev_pixel_loc[0] + area
    for i in range(0 if x < 0 else x, height if y > height else y):
        if red(pixels[width_pixel, i]):
            pixel_loc.append(i)
            break
    if len(pixel_loc) < 1:
        pixel_loc.append(prev_pixel_loc[0])

    x = prev_pixel_loc[1] - area
    y = prev_pixel_loc[1] + area
    for i in range(0 if x < 0 else x, height if y > height else y):
        if yellow(pixels[width_pixel, i]):
            pixel_loc.append(i)
            break
    if len(pixel_loc) < 2:
        pixel_loc.append(prev_pixel_loc[1])

    x = prev_pixel_loc[2] - area
    y = prev_pixel_loc[2] + area
    for i in range(0 if x < 0 else x, height if y > height else y):
        if green(pixels[width_pixel, i]):
            pixel_loc.append(i)
            break
    if len(pixel_loc) < 3:
        pixel_loc.append(prev_pixel_loc[2])

    x = prev_pixel_loc[3] - area
    y = prev_pixel_loc[3] + area
    for i in range(0 if x < 0 else x, height if y > height else y):
        if blue(pixels[width_pixel, i]):
            pixel_loc.append(i)
            break
    if len(pixel_loc) < 4:
        pixel_loc.append(prev_pixel_loc[3])

    return pixel_loc
def color(pixel_loc, width_pixel, pixels, height):
    if len(pixel_loc) != 4:
        for i in range(height):
            pixels[width_pixel, i] = 0
    else:
        for i in range(pixel_loc[0]):
            pixels[width_pixel, i] = 0
        for i in range(pixel_loc[0], pixel_loc[1]):
            pixels[width_pixel, i] = 60
        for i in range(pixel_loc[1], pixel_loc[2]):
            pixels[width_pixel, i] = 120
        for i in range(pixel_loc[2], pixel_loc[3]):
            pixels[width_pixel, i] = 180
        for i in range(pixel_loc[3], height):
            pixels[width_pixel, i] = 240


def color_layers(image):
    img = image.convert('L')
    pixels = image.load()
    pixels_greyscale = img.load()
    prev_pixel_loc = []
    width = img.size[0]
    height = img.size[1]

    j = 0
    while j < width:
        i = 0
        prev_pixel_loc = []

        while i < height:
            if red(pixels[j, i]):
                prev_pixel_loc.append(i)
                break
            i = i + 1
        while i < height:
            if yellow(pixels[j, i]):
                prev_pixel_loc.append(i)
                break
            i = i + 1
        while i < height:
            if green(pixels[j, i]):
                prev_pixel_loc.append(i)
                break
            i = i + 1
        while i < height:
            if blue(pixels[j, i]):
                prev_pixel_loc.append(i)
                break
            i = i + 1

        color(prev_pixel_loc, j, pixels_greyscale, height)
        if len(prev_pixel_loc) == 4:
            break
        j = j + 1

    for i in range(j + 1, width):
        pixel_loc = find_borders(i, pixels, prev_pixel_loc, img)
        color(pixel_loc, i, pixels_greyscale, height)
        prev_pixel_loc = pixel_loc
    return img


import os
import shutil

dirs = os.listdir("slojevi kompletno")

train_path = "data/membrane/train/image"
os.makedirs(train_path)
test_path = "data/membrane/test_zaprave"
os.makedirs(test_path)
valid_path = "data/membrane/test"
os.makedirs(valid_path)
train_masks_path = "data/membrane/train/label"
os.makedirs(train_masks_path)
valid_masks_path = "data/membrane/test/expected"
os.makedirs(valid_masks_path)
dir_counter = 0
traincnt = testcnt = trainlabelcnt = testlabelcnt = validcnt = 0
for dir in dirs:

    dir_counter += 1
    originals_path = os.path.join("slojevi kompletno", dir, "neobrađene 8 bit")
    originals = os.listdir(originals_path)
    processed_path = os.path.join("slojevi kompletno", dir, "obrađene RGB", "slojevi")
    for file in originals:
        orig_path = os.path.join(originals_path, file)
        proc_path = os.path.join(processed_path, file)
        if (not os.path.isfile(proc_path)):
            orig_dest_path = os.path.join(test_path, str(testcnt) + '.tif')
            testcnt = testcnt + 1
            shutil.copyfile(orig_path, orig_dest_path)
            continue
        if (dir_counter <= 20):
            orig_dest_path = os.path.join(train_path, str(traincnt) + '.tif')
            traincnt = traincnt + 1
        else:
            orig_dest_path = os.path.join(valid_path, str(validcnt) + '.tif')
            validcnt = validcnt + 1
        shutil.copyfile(orig_path, orig_dest_path)
        image = Image.open(proc_path)

        img = color_layers(image)

        if (dir_counter <= 20):
            path = os.path.join(train_masks_path, str(trainlabelcnt) + '.tif')
            trainlabelcnt = trainlabelcnt + 1
        else:
            path = os.path.join(valid_masks_path, str(testlabelcnt) + '.tif')
            testlabelcnt = testlabelcnt + 1
        img.save(path)