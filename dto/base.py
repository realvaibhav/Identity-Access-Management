from typing import Optional, List, Dict, Union
from pydantic import BaseModel

class ResponseState(BaseModel):
    pass

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class SingleResponse(ResponseState):
    data: Dict = {}
    
class Metadata(BaseModel):
    count: int
    limit: int
    offset: int
    
class ListResponse(ResponseState):
    data: List = []
    metadata: Optional[Metadata] = None

class ErrorResponse(ResponseState):
    error_msg: str