from PIL import Image
import os
import numpy as np
from sklearn.metrics import confusion_matrix


def dice_loss(result_path, label_path, size):
    result = Image.open(result_path)
    label = Image.open(label_path)
    label.thumbnail(size, Image.ANTIALIAS)
    label = np.matrix.round(np.asarray(label) / 60)
    result = np.matrix.round(np.asarray(result) / 16000)
    result = result.flatten()
    label = label.flatten()
    return confusion_matrix(label, result).ravel().reshape(5, 5)


size = 256, 512

result_folder = 'data/membrane/test/results'
label_folder = 'data/membrane/test/expected'
results = os.listdir(result_folder)
labels = os.listdir(label_folder)
conf_matrix = np.zeros([5, 5])
accs = np.zeros([5, np.size(results)])
print(np.size(results))
k = 0
for result, label in zip(results, labels):
    conf_matrix = dice_loss(os.path.join(result_folder, result), os.path.join(label_folder, label), size=(256, 512))
    for k in range(5):
        tp = fp = tn = fn = 0
        for i in range(5):
            for j in range(5):
                if (i == k and j == k):
                    tp = conf_matrix[i, j]
                elif (i == k and j != k):
                    # TODO
                    continue
                elif (i != k and j == k):
                    # TODO
                    continue
                else:
                    # TODO
                    continue

print(np.matrix.round(conf_matrix / np.size(results), 3))
