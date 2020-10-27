import torch, torchvision
import json

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import cv2, os, itertools

# os.environ["CUDA_VISIBLE_DEVICES"]=""
im = cv2.imread("./input.jpg")
height, width, _ = im.shape
# print(f"height: {height} and width : {width}")

#####################################
### Object detection
#####################################

# Create config
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")

# Create predictor
predictor = DefaultPredictor(cfg)

# Make prediction
outputs = predictor(im)

v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
plt.figure(figsize = (14, 10))
plt.imshow(cv2.cvtColor(v.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
plt.show()

#####################################
### Instance Segmentation
#####################################

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

# Create predictor
predictor = DefaultPredictor(cfg)

# Make prediction
outputs = predictor(im)
# print(outputs)
# look at the outputs. See https://detectron2.readthedocs.io/tutorials/models.html#model-output-format for specification
# print(outputs["instances"].pred_classes)
# print(outputs["instances"].pred_boxes)

output_pred_classes = outputs["instances"].pred_classes
output_pred_boxes = outputs["instances"].pred_boxes
output_pred_scores = outputs["instances"].scores

# print(output_pred_classes.cpu().numpy())
# print(output_pred_boxes[0].__iter__())

list_pred_classes = output_pred_classes.cpu().numpy()
list_pred_scores = output_pred_scores.cpu().numpy()

list_pred_boxes = []
for i in output_pred_boxes.__iter__():
    list_pred_boxes.append(i.cpu().numpy())
    
with open('coco-labels.json') as f:
    data_from_coco = json.load(f)

data_length = len(output_pred_classes.cpu().numpy())

output_all_item = {}
output_list = []

for i in range(data_length):
    
    # Loop to get classes from coco json
    item_pred_classes = list_pred_classes[i]
    item_pred_classes = data_from_coco[f"{item_pred_classes}"]
    
    # Loop to get bounding box
    item_pred_boxes = list_pred_boxes[i]
    
    ##### Scale the coordinates 
    
    x1, y1, x2, y2 = item_pred_boxes[0], item_pred_boxes[1], item_pred_boxes[2], item_pred_boxes[3]
    
    x1 = "{x1:.4f}".format(x1= x1 / width)
    x2 = "{x2:.4f}".format(x2= x2 / width)
    y1 = "{y1:.4f}".format(y1= y1 / height)
    y2 = "{y2:.4f}".format(y2= y2 / height)
    
    item_pred_boxes = [x1, y1, x2, y2]
    
    # Loop to get probability 
    item_pred_scores = list_pred_scores[i]
    item_pred_scores = "{p:.2f}".format(p=item_pred_scores*100)
    
    # Insert class and box into dict
    output_each_item = {
        "label": f"{item_pred_classes}",
        "coordinate": item_pred_boxes,
        "prob": f"{item_pred_scores}",
        "image_size": {
            "height": f"{height}",
            "width": f"{width}"
        }
    }
    
    output_list.append(output_each_item)

# print(output_list)