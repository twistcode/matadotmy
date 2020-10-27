import cv2
import base64
import io
import json
import torch
import numpy as np

from typing import List

from PIL import Image
from pydantic import BaseModel
from fastapi import FastAPI

from torchvision import transforms

from efficientnet_pytorch import EfficientNet

app = FastAPI()

##############################
### Load Model beforehand

model = EfficientNet.from_pretrained('efficientnet-b0')
model.eval()

# Preprocess image
tfms = transforms.Compose([transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),])

### Load ImageNet class names
labels_map = json.load(open('imagenet-classes.json'))
labels_map = [labels_map[i] for i in range(1000)]
    
##############################

##############################
### image base 64

class ImageBase64(BaseModel):
    image: str
    
##############################

##############################
### Output response

class Output(BaseModel):
    prob: str
    label: str
    
##############################

@app.get("/")
async def hello():
    return {"service": "twistcode image classification service"}

@app.post("/inference")
async def inference(imageBase64: ImageBase64):
    
    imgdata = base64.b64decode(imageBase64.image)
    image = Image.open(io.BytesIO(imgdata))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = tfms(img).unsqueeze(0)
    
    with torch.no_grad():
        outputs = model(img)
        
    # Print predictions
    output_list = []
    for idx in torch.topk(outputs, k=5).indices.squeeze(0).tolist():
        prob = torch.softmax(outputs, dim=1)[0, idx].item()
        # print('{label:<75} ({p:.2f}%)'.format(label=labels_map[idx], p=prob*100))
        labels = labels_map[idx]
        prob = "{p:.2f}".format(p=prob*100)
        
        output = Output(label=labels, prob=prob)
        output_list.append(output.dict())
    
    return {"data": output_list}
    