from datetime import datetime
from pydantic import BaseModel, Field, validator
from bson.objectid import ObjectId
from typing import Optional
from dto.permissions import AccessLevelEnum


class PermissionModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    user_id: str
    organisation_id: str
    access_level: AccessLevelEnum
    created_at: datetime = Field(None)
    updated_at: datetime = Field(None)
    
    
    @validator('id', pre=True, always=True)
    def id_to_str(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value
    

    class Config:
        collection = "permissions"
        orm_mode = True
