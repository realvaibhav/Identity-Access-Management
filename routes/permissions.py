from fastapi import APIRouter
from typing import List
from dto.permissions import AccessLevelEnum
from dto.base import SingleResponse
from services.permissions import create_permissions, update_permissions, delete_permissions

router = APIRouter()


@router.post("/api/permissions/{organisation_id}", tags=["permissions"], response_model=SingleResponse)
async def create_new_permission(organisation_id: str, user_ids: List[str], access_level: AccessLevelEnum) -> SingleResponse:
    return create_permissions(organisation_id, user_ids, access_level)


@router.put("/api/permissions/{organisation_id}", tags=["permissions"], response_model=SingleResponse)
async def update_existing_permission(organisation_id: str, user_ids: List[str], access_level: AccessLevelEnum) -> SingleResponse:
    return update_permissions(organisation_id, user_ids, access_level)


@router.delete("/api/permissions/{organisation_id}", tags=["permissions"], response_model=SingleResponse)
async def delete_existing_permission(organisation_id: str, user_ids: List[str]) -> SingleResponse:
    return delete_permissions(organisation_id, user_ids)
