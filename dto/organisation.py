from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from bson import ObjectId
from dto.permissions import AccessLevelEnum


class OrganisationArgs(BaseModel):
    name: str


class OrganisationState(OrganisationArgs):
    id: str = Field(primary_field=True, alias="_id")
    created_at: datetime
    updated_at: datetime

    @validator('id', pre=True, always=True)
    def id_to_str(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value


class OrganisationPermissionState(OrganisationArgs):
    organisation_id: str = Field(None)
    access_level: AccessLevelEnum
    
    @validator('organisation_id', pre=True, always=True)
    def id_to_str(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value