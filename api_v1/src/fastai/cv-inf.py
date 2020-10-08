from fastai.vision.all import *
from fastai.vision import *
import os, cv2

# path = Path("/home/hasif/work/matadotmy/src/fastai/models")
# print(path)
# learn = load_learner("models/export.pkl")

# def label_func(f): return f[0].isupper()

learn = load_learner("models/export_multi.pkl")

image = load_image("yorkshire_terrier_99.jpg")
img = cv2.imread("yorkshire_terrier_99.jpg")
# im = PIL.Image.open("yorkshire_terrier_99.jpg")
# print(image2tensor(image))
# print(im)
# dls = ImageDataLoaders.from_name_func(path, files, label_func, item_tfms=Resize(224))

# learn = cnn_learner(dls, resnet34, metrics=error_rate)
# print(img.shape)

print(learn.predict(img))