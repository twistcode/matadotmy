import cv2
import base64
import io
import json
import numpy as np

from typing import List

from PIL import Image
from pydantic import BaseModel
from fastapi import FastAPI

from torchvision import transforms

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
# from detectron2.utils.visualizer import Visualizer
# from detectron2.data import MetadataCatalog

app = FastAPI()

##############################
### Load Model beforehand

cfg = get_cfg()
cfg.MODEL.DEVICE = "cpu"
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

# Create predictor
predictor = DefaultPredictor(cfg)

# Preprocess image
tfms = transforms.Compose([transforms.Resize(224), transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),])

    
##############################

##############################
### image base 64

class ImageBase64(BaseModel):
    image: str
    
##############################

@app.get("/")
async def hello():
    return {"service": "twistcode object detection service"}

@app.post("/inference")
async def inference(imageBase64: ImageBase64):
    
    imgdata = base64.b64decode(imageBase64.image)
    image = Image.open(io.BytesIO(imgdata))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    # img = Image.fromarray(img)
    # img = tfms(img).unsqueeze(0)
    
    ##################################################

    height, width, _ = img.shape

    #####################################
    ### Instance Segmentation
    #####################################

    # Make prediction
    outputs = predictor(img)
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
    
    return {"data": output_list}
    