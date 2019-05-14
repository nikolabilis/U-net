import os
import shutil
from PIL import Image


dirs = os.listdir('slojevi maske')


for dir in dirs:

    print(dir)
    originals_path = os.path.join("slojevi maske", dir, "originali")
    mask_path = os.path.join("slojevi maske", dir, "maske")

    original_files = os.listdir(originals_path)
    mask_files = os.listdir(originals_path)

    i = 0

    for file in original_files:
        os.rename(os.path.join(originals_path,file), str(originals_path)+"/" + str(i)+ '.tif')
        i = i + 1
    i =0
    for file in mask_files:
        os.rename(os.path.join(mask_path,file), str(mask_path)+"/" + str(i)+ '.tif')
        i = i + 1
