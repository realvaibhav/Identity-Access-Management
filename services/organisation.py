from typing import Optional
from datetime import datetime, timezone
from fastapi import HTTPException
from bson.objectid import ObjectId
from dto.organisation import OrganisationArgs
from model.organisation import OrganisationModel
from dto.base import SingleResponse, ListResponse
from dto.user import UserPermissionState
from settings.database import organisation_collection, user_collection, permissions_collection
from datetime import datetime, timezone
from utils.types import CustomException
from utils.validators import Validator


def create_organisation(org: OrganisationArgs) -> SingleResponse:
    try:
        Validator.is_duplicate_org(org.name)
        organisation_dict = org.dict()
        organisation_dict['created_at'] = datetime.now(timezone.utc)
        organisation_dict['updated_at'] = datetime.now(timezone.utc)
        new_organisation = organisation_collection.insert_one(
            organisation_dict)
        if new_organisation is None:
            raise Exception("Failed to create new Organisation")
        organisation_dict['_id'] = str(new_organisation.inserted_id)
        return SingleResponse(data=OrganisationModel(**organisation_dict))
    except CustomException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_many_organisation(name: Optional[str], limit: int, offset: int) -> ListResponse:
    try:
        query = {}
        if name:
            query['name'] = {'$regex': name}
        organisations = organisation_collection.find(
            query).skip(offset).limit(limit)
        count = organisation_collection.count_documents(query)
        metadata = {
            'count': count,
            'limit': limit,
            'offset': offset,
        }
        return ListResponse(data=[OrganisationModel(**org) for org in organisations], metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_one_organisation(organisation_id: str) -> SingleResponse:
    try:
        organisation = organisation_collection.find_one(
            {'_id': ObjectId(organisation_id)})
        if not organisation:
            raise CustomException(
                status_code=404, detail="Organisation not found")
        return SingleResponse(data=OrganisationModel(**organisation))
    except CustomException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_users_by_org_id(organisation_id: str, limit: int, offset: int) -> ListResponse:
    try:
        Validator.check_org(organisation_id)
        users = []
        query = {
            "organisation_id": organisation_id
        }
        for permission in permissions_collection.find(query).skip(offset).limit(limit):
            user = user_collection.find_one(
                {"_id": ObjectId(permission["user_id"])})
            if user:
                users.append(UserPermissionState(
                    user_id=user["_id"], name=user["name"], email=user["email"], access_level=permission["access_level"]))

        count = permissions_collection.count_documents(query)

        metadata = {
            'count': count,
            'limit': limit,
            'offset': offset,
        }

        return ListResponse(data=users, metadata=metadata)

    except CustomException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
