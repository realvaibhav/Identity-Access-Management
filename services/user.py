import re
from typing import Optional
from datetime import datetime, timezone
from fastapi import HTTPException
from bson.objectid import ObjectId
from model.user import UserModel
from dto.user import UserArgs
from dto.organisation import OrganisationPermissionState
from dto.base import SingleResponse, ListResponse, ErrorResponse
from settings.database import user_collection, permissions_collection, organisation_collection
from datetime import datetime, timezone
from utils.validators import Validator
from utils.types import CustomException


def create_user(user: UserArgs) -> SingleResponse:

    try:
        Validator.is_duplicate_email(user.email)
        user_dict = user.dict()
        user_dict['created_at'] = datetime.now(timezone.utc)
        user_dict['updated_at'] = datetime.now(timezone.utc)
        new_user = user_collection.insert_one(user_dict)
        if new_user is None:
            raise Exception("Failed to insert user")
        user_dict['_id'] = str(new_user.inserted_id)
        return SingleResponse(data=UserModel(**user_dict))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_many_user(email: Optional[str], limit: int, offset: int) -> ListResponse:
    try:
        query = {}
        if email:
            query['email'] = {'$regex': email}
        users = user_collection.find(query).skip(offset).limit(limit)
        count = user_collection.count_documents(query)
        metadata = {
            'count': count,
            'limit': limit,
            'offset': offset,
        }
        return ListResponse(data=[UserModel(**user) for user in users], metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_one_user(user_id: str) -> SingleResponse:
    try:
        user = user_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return SingleResponse(data=UserModel(**user))
    except HTTPException as e:
        error_msg = e.detail
        status_code = e.status_code
        return ErrorResponse(status_code=status_code, error_msg=error_msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_organisations_by_user_id(user_id: str, limit: int, offset: int) -> ListResponse:
    try:
        Validator.check_user(user_id)
        organisations = []
        query = {
            "user_id": user_id
        }
        for permission in permissions_collection.find(query).skip(offset).limit(limit):
            organisation = organisation_collection.find_one(
                {"_id": ObjectId(permission["organisation_id"])})
            if organisation:
                organisations.append(OrganisationPermissionState(
                    organisation_id=organisation["_id"], name=organisation["name"], access_level=permission["access_level"]))

        count = permissions_collection.count_documents(query)

        metadata = {
            'count': count,
            'limit': limit,
            'offset': offset,
        }

        return ListResponse(data=organisations, metadata=metadata)

    except CustomException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
