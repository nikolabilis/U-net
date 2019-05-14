from model import *
from data import *
import numpy

os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3,4"

loss_file = open('loss.txt', 'a')
myGene = trainGenerator(2, 'data/membrane/train', 'image', 'label', dict(), save_to_dir=None,
                        target_size=(512, 256), num_class=5, flag_multi_class=True)

model = unet(input_size=(512, 256, 1))
model_checkpoint = ModelCheckpoint('unet_membrane.hdf5', monitor='loss', verbose=1, save_best_only=True)
history = model.fit_generator(myGene, steps_per_epoch=300, epochs=3, callbacks=[model_checkpoint])

loss_history = history.history["loss"]
numpy_loss_history = numpy.array(loss_history)
loss_file.writelines(str(numpy_loss_history))
loss_file.close()
# Validacija
num_of_test_files = np.size(os.listdir('data/membrane/test')) - 2

testGene = testGenerator("data/membrane/test", flag_multi_class=True, num_image=num_of_test_files,
                         target_size=(512, 256, 1))

results = model.predict_generator(testGene, num_of_test_files, verbose=1)
saveResult("data/membrane/test/results", results)

# Testiranje
num_of_test_files = np.size(os.listdir('data/membrane/test_zaprave')) - 1

testGene = testGenerator("data/membrane/test_zaprave", flag_multi_class=True, num_image=num_of_test_files,
                         target_size=(512, 256, 1))

results = model.predict_generator(testGene, num_of_test_files, verbose=1)
saveResult("data/membrane/test_zaprave/results", results)
