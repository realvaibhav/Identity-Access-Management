from datetime import datetime
from pydantic import BaseModel, Field, validator
from bson.objectid import ObjectId
from typing import Optional

class OrganisationModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str = Field(None, index=True)
    created_at: datetime = Field(None)
    updated_at: datetime = Field(None)
    
    
    @validator('id', pre=True, always=True)
    def id_to_str(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    class Config:
        collection = "organisations"
        orm_mode = True
