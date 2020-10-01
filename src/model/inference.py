from typing import Optional, List
from pydantic import BaseModel, Field
from src.db.database import PyObjectId
from bson import ObjectId

class Data(BaseModel):
    image_path: str

class Inference(BaseModel):
    node_ip: str
    service_id: str
    model_id: str
    data: Optional[List[Data]] = None
    