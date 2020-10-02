from fastai.vision.all import *
import os

# os.environ['TORCH_HOME'] = '~/home/hasif/work/matadotmy/src/fastai/models'

path = untar_data(URLs.PETS)
print(path.ls())

files = get_image_files(path/"images")
print(len(files))

def label_func(f): return f[0].isupper()

dls = ImageDataLoaders.from_name_func(path, files, label_func, item_tfms=Resize(224))

learn = cnn_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(1)

learn.model_dir = "/home/hasif/work/matadotmy/src/fastai/models"
learn.save("test")
# learn.export(file = Path("models/export.pkl"))

learn.predict(files[0])