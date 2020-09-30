from typing import Optional, List
from pydantic import BaseModel

class Data(BaseModel):
    image_path: str


class Inference(BaseModel):
    node_ip: str
    service_id: str
    model_id: str
    data: Optional[List[Data]] = None