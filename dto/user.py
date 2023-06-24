from pydantic import BaseModel, Field, validator
from typing import Optional
from utils.validators import Validator
from datetime import datetime, timezone
from bson import ObjectId
from .permissions import AccessLevelEnum


class UserArgs(BaseModel):
    name: str
    email: str

    @validator('email')
    def email_validator(cls, value):
        return Validator().is_valid_email(value)


class UserPermissionState(UserArgs):
    user_id: str = Field(None)
    access_level: AccessLevelEnum

    @validator('user_id', pre=True, always=True)
    def id_to_str(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value