from typing import List
from fastapi import HTTPException
from dto.permissions import AccessLevelEnum
from dto.base import SingleResponse
from model.permissions import PermissionModel
from settings.database import permissions_collection
from utils.validators import Validator
from utils.types import CustomException
from pymongo import InsertOne, ReplaceOne, DeleteOne


def create_permissions(organisation_id: str, user_ids: List[str], access_level: AccessLevelEnum) -> SingleResponse:
    try:
        organisation = Validator.check_org(organisation_id)
        Validator.check_access_level(access_level)
        Validator.check_users(user_ids)

        existing_permissions = permissions_collection.find(
            {"user_id": {"$in": user_ids}, "organisation_id": organisation_id})
        existing_permissions_map = {
            existing_permission["user_id"]: existing_permission for existing_permission in existing_permissions}

        bulk_operations = []
        for user_id in user_ids:
            existing_permission = existing_permissions_map.get(user_id)
            if existing_permission:
                raise CustomException(
                    status_code=409, detail=f"Permission already exists for user {user_id} in organization {organisation_id}")

            permission = PermissionModel(
                user_id=user_id, organisation_id=organisation_id, access_level=access_level.value)
            bulk_operations.append(InsertOne(permission.dict()))

        if bulk_operations:
            permissions_collection.bulk_write(bulk_operations)

        response = {
            'message': f"{len(user_ids)} user(s) successfully added to {organisation['name']}"
        }

        return SingleResponse(data=response)
    except CustomException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_permissions(organisation_id: str, user_ids: List[str], access_level: AccessLevelEnum) -> SingleResponse:
    try:
        organisation = Validator.check_org(organisation_id)
        Validator.check_access_level(access_level)
        Validator.check_users(user_ids)

        existing_permissions = permissions_collection.find(
            {"user_id": {"$in": user_ids}, "organisation_id": organisation_id})
        existing_permissions_map = {
            existing_permission["user_id"]: existing_permission for existing_permission in existing_permissions}

        bulk_operations = []
        for user_id in user_ids:
            existing_permission = existing_permissions_map.get(user_id)
            if not existing_permission:
                raise CustomException(
                    status_code=404, detail=f"Permission not found for user {user_id} in organization {organisation_id}")

            updated_permission = PermissionModel(
                id=existing_permission['_id'], created_at=existing_permission['created_at'], user_id=user_id, organisation_id=organisation_id, access_level=access_level.value)

            bulk_operations.append(ReplaceOne(
                filter={"_id": existing_permission['_id']},
                replacement=updated_permission.dict()
            ))

        if bulk_operations:
            permissions_collection.bulk_write(bulk_operations)

        response = {
            'message': f"{len(user_ids)} user(s) updated in {organisation['name']}"
        }

        return SingleResponse(data=response)

    except CustomException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_permissions(organisation_id: str, user_ids: List[str]) -> SingleResponse:
    try:
        organisation = Validator.check_org(organisation_id)
        Validator.check_users(user_ids)

        existing_permissions = permissions_collection.find(
            {"user_id": {"$in": user_ids}, "organisation_id": organisation_id})
        existing_permissions_map = {
            existing_permission["user_id"]: existing_permission for existing_permission in existing_permissions}

        bulk_operations = []
        for user_id in user_ids:
            existing_permission = existing_permissions_map.get(user_id)
            if not existing_permission:
                raise CustomException(
                    status_code=404, detail=f"Permission not found for user {user_id} in organization {organisation_id}")

            bulk_operations.append(DeleteOne(
                filter={"_id": existing_permission['_id']},
            ))

        if bulk_operations:
            permissions_collection.bulk_write(bulk_operations)

        response = {
            'message': f"Permission deleted for {len(user_ids)} user(s) in organization {organisation['name']}"
        }

        return SingleResponse(data=response)

    except CustomException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
