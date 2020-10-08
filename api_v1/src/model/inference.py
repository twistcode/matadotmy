from typing import List
from pydantic import BaseModel, Field
# from src.db.database import PyObjectId
# from bson import ObjectId
# from datetime import datetime as dt

# class ServiceID(BaseModel):
#     service_id: str
#     service_type: str
    
# serviceid = ServiceID(service_id='1234', service_type='inference')
# print(serviceid)

# class ModelID(BaseModel):
#     model_id: str
#     path: str
    
class Data(BaseModel):
    image_path: str

class Inference(BaseModel):
    node_ip: List[str]
    service_id: str
    model_id: str
    description: str
    data: List[str] = None
    
    