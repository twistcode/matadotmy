from typing import Optional, List

from fastapi import FastAPI, File, UploadFile, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from datetime import datetime

from starlette.status import HTTP_200_OK
from starlette.responses import Response

from model.inference import Data, Inference

from pymongo import MongoClient

from fastai.vision.all import *
import cv2
# from fastai.vision import *

import timeit

client = MongoClient()
db = client.lulu

app = FastAPI()

###############################

# "node_ip": "192.1.1.1",
# "service_id": "1234",
# "image_path": f"{img_path}",
# "classified_as": f"{classified_as}",
# "probability": f"{inference_probability}"
            
class OutputResponse(BaseModel):
    node_ip: str
    service_id: str
    image_path: str
    classified_as: str
    probability: str
    
#############################


@app.get("/")
async def hello_world():
    return "hello world"

@app.post("/ping")
async def ping():
    return "pong"

@app.post("/inference")
async def inference(inference: Inference, status_code=HTTP_200_OK):
    
    #####################################################################
    ############## Get data #############################################
    #####################################################################
    
    # Check inference services from db
    # Image classification / object detection / image segmentation

    #####################################################################
    
    try:
        service = db.services.find_one({ "service_id": f"{inference.service_id}" })
        service_type = service["service_type"]
    except Exception as e:
        return "lol"
        
    # print(service_type)
    
    try:
        model = db.models.find_one({ "model_id": f"{inference.model_id}" })
        model_path = model["model_path"]
    except Exception as e:
        print("An exception occurred ::", e)
    # print(model_path)

    #####################################################################
    ############## Inference ############################################
    #####################################################################
    
    if service_type == "inference":
        # print(model_path)
        learn = load_learner(f"{model_path}")
        
        # print(inference.data[0])
        img_path = inference.data[0]
        img = cv2.imread(img_path)
        
        out = learn.predict(img)
        # print(out)
        # print(max(out[2]).cpu().detach().numpy())

        classified_as = out[0]
        inference_probability = max(out[2].cpu().detach().numpy())
    
    #####################################################################
    ############## Store inference output ###############################
    #####################################################################
    
        output_response = OutputResponse(
            node_ip="192.1.1.1",
            service_id="1234",
            image_path=f"{img_path}",
            classified_as=f"{classified_as}",
            probability=f"{inference_probability}"
        )
    
        db.output.insert_one(output_response.dict())
        
        json_test = jsonable_encoder(output_response)
        # print("JSON TEST : ", json_test)
    return JSONResponse(content=json_test)

# @app.post("/file")
# async def test_file(response: Response, file: bytes = File(...)):
#     response.headers["x-file-size"] = str(len(file))
#     response.set_cookie(key="cookie-api", value="test")
#     return {"file_size": len(file)}

# @app.post("/upload/file")
# async def upload_file(file: UploadFile = File(...)):
#     return {"file_size": file.filename}