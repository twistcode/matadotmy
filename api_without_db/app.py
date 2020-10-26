from api_v1.src.app import inference
from typing import Optional, List

from fastapi import FastAPI, File, UploadFile, Response, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from datetime import datetime

from starlette.status import HTTP_200_OK
from starlette.responses import Response

from fastai.vision.all import *
import cv2

import cv2
import shutil
import numpy as np

###############################
### OUTPUT RESPONSE

# "node_ip": "192.1.1.1",
# "service_id": "1234",
# "image_path": f"{img_path}",
# "classified_as": f"{classified_as}",
# "probability": f"{inference_probability}"
            
# class OutputResponse(BaseModel):
#     node_ip: str
#     service_id: str
#     image_path: str
#     classified_as: str
#     probability: str
    
#############################
### INPUT RESPONSE

# class Data(BaseModel):
#     image_path: str

# class Inference(BaseModel):
#     node_ip: Optional[str]
#     service_id: str
#     model_id: str
#     description: str
#     data: List[str] = None
    
#############################

# def checkServiceAndGetModel(service_id):
#     if inference.service_id == "twistcode-image-classification":
#         model = inference.model_id
#         model = model["model_path"]
#     return model

app = FastAPI()

@app.get("/")
async def hello_world():
    return "hello world"

@app.post("/inference")
async def inference(inference: Inference, status_code=HTTP_200_OK):
    learn
    
    
    
    return {"inference": "succesful"}

# @app.post("/file")
# async def test_file(response: Response, file: bytes = File(...)):
#     # response.headers["x-file-size"] = str(len(file))
#     # response.set_cookie(key="cookie-api", value="test")
#     with open("destination.png", "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
    
#     # img = cv2.imread(file)
#     # print(img.shape)
#     return {"file_size": len(file)}

# @app.post("/upload/file")
# async def upload_file(file: UploadFile = File(...), token: str = Form(...)):
#     # with open("destination.png", "wb") as buffer:
#     #     shutil.copyfileobj(file.file, buffer)
#     contents = await file.read()
#     nparr = np.fromstring(contents, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     print(img)
#     # img_dimensions = str(img.shape)
#     # print(img_dimensions)
    
#     return {"file_size": file.filename}