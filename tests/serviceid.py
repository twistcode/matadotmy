from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime as dt

class ServiceID(BaseModel):
    service_id: str
    service_type: str
    date_created: Optional[dt] = dt.utcnow()
    date_deleted: Optional[dt] = None
    
serviceid = ServiceID(service_id='1234', service_type='inference')
print(serviceid)