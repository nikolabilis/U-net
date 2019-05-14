import os
from PIL import Image
import numpy as np


def split_training_data():
    dest_test_folder = os.path.join("data/membrane/test")
    dest_expected_folder = os.path.join("data/membrane/test/expected")
    dest_result_folder = os.path.join("data/membrane/test/results")
    dest_train_folder = os.path.join("data/membrane/train/image")
    dest_label_folder = os.path.join("data/membrane/train/label")
    dirs = os.listdir('slojevi maske')
    cnt_train = 0
    cnt_test = 0
    # Izbriši sve trenutno u train, label i result
    for file in os.listdir(dest_test_folder):
        file_path = os.path.join(dest_test_folder, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    for file in os.listdir(dest_train_folder):
        file_path = os.path.join(dest_train_folder, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    for file in os.listdir(dest_label_folder):
        file_path = os.path.join(dest_label_folder, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)


    for file in os.listdir(dest_expected_folder):
        file_path = os.path.join(dest_expected_folder, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

    for file in os.listdir(dest_result_folder):
        file_path = os.path.join(dest_result_folder, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    i = 0
    for dir in dirs:
        train = True
        originals_path = os.path.join("slojevi maske", dir, "originali")
        mask_path = os.path.join("slojevi maske", dir, "maske")
        for file1 in os.listdir(originals_path):
            for file2 in os.listdir(mask_path):
                if (file1 == file2):
                    if i % 5 != 0:
                        dest_original_path = os.path.join(dest_train_folder, str(cnt_train) + ".tif")
                        dest_mask_path = os.path.join(dest_label_folder, str(cnt_train) + ".tif")
                        train = True
                    else:
                        dest_original_path = os.path.join(dest_test_folder, str(cnt_test) + ".tif")
                        dest_mask_path = os.path.join(dest_expected_folder, str(cnt_test) + ".tif")
                        train = False
                    imgOrig = Image.open(os.path.join(originals_path, file1))
                    imgMask = Image.open(os.path.join(mask_path, file2))
                    if(np.unique(np.asarray(imgMask))<6):
                        imgOrig.save(dest_original_path)
                        imgMask.save(dest_mask_path)
                        if(train):
                            cnt_train = cnt_train + 1
                        else:
                            cnt_test = cnt_test + 1
                    break
        i = i+1
split_training_data()
