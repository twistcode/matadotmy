from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional

class testmongo(Document):
    name = StringField()
    age = IntField()

class testpydantic(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name: str
    age: int
    
class PyObjectId(ObjectId):
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')
    
client = MongoClient()
db = client['fastapi']

testpyd = testpydantic(
    id=
)
ret = db.insert_one()
    

    