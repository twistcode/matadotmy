from fastai.vision.all import *
from fastai.vision import *
from fastai.metrics import error_rate
import os

# os.environ['TORCH_HOME'] = '~/home/hasif/work/matadotmy/src/fastai/models'

path = untar_data(URLs.PETS)
print(path.ls())

files = get_image_files(path/"images")
print(len(files))

# def label_func(f): return f[0].isupper()

# pat = r'^(.*)_\d+.jpg'

# dls = ImageDataLoaders.from_name_func(path, files, pat, item_tfms=Resize(224))
# print(dls.__dict__)
# print(dls.loaders)
# learn = cnn_learner(dls, resnet34, metrics=error_rate)
# learn.fine_tune(1)

# learn.model_dir = "/home/hasif/work/matadotmy/src/fastai/models"
# # learn.save("test")
# learn.export("/home/hasif/work/matadotmy/src/fastai/models/export.pkl")
# # learn.export(file = Path("models/export.pkl"))

# print(learn.classes())
# learn.predict(files[0])

###############################

pat = r'^(.*)_\d+.jpg'

dls = ImageDataLoaders.from_name_re(path, files, pat, item_tfms=Resize(460),
                                    batch_tfms=aug_transforms(size=224))

learn = cnn_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(1, 3e-3)
learn.export("/home/hasif/work/matadotmy/src/fastai/models/export_multi.pkl")
print(learn.predict(files[0]))
# interp = Interpretation.from_learner(learn)

##########################################################

# path_anno = path/'annotations'
path_img = f"{path}/images"
print(path_img)

# fnames = get_image_files(path_img)
# # print(fnames[:5])


# np.random.seed(2)
# pat = r'/([^/]+)_\d+.jpg$'


# data = ImageDataBunch.from_name_re(path_img, fnames, pat, ds_tfms=get_transforms(), size=224, bs=bs
#                                   ).normalize(imagenet_stats)