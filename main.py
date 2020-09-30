from typing import Optional, List

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

from datetime import datetime

from starlette.status import HTTP_200_OK
from starlette.responses import Response

class Data(BaseModel):
    image_path: str


class Inference(BaseModel):
    node_ip: str
    service_id: str
    model_id: str
    data: Optional[List[Data]] = None

# d = Data(image_path = "/lala")
# print(d.schema())

app = FastAPI()

@app.get("/")
async def hello_world():
    return "hello world"

@app.post("/ping")
async def ping():
    return "pong"

@app.post("/inference")
async def inference(inference: Inference, status_code=HTTP_200_OK):

    test_data = inference.data[0]
    print(test_data.image_path)
    return "Hello world"

@app.post("/file")
async def test_file(response: Response, file: bytes = File(...)):
    response.headers["x-file-size"] = str(len(file))
    response.set_cookie(key="cookie-api", value="test")
    return {"file_size": len(file)}

@app.post("/upload/file")
async def upload_file(file: UploadFile = File(...)):
    return {"file_size": file.filename}