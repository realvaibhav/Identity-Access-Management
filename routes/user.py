from fastapi import APIRouter
from typing import Optional
from dto.user import UserArgs
from dto.base import SingleResponse, ListResponse
from services.user import create_user, get_many_user, get_one_user, get_organisations_by_user_id

router = APIRouter()


@router.post("/api/user/", tags=["user"], response_model=SingleResponse)
async def create_new_user(user: UserArgs) -> SingleResponse:
    return create_user(user)


@router.get("/api/user/", tags=["user"], response_model=ListResponse)
async def get_users_by_filters(email: Optional[str] = None, limit: int = 10, offset: int = 0) -> ListResponse:
    return get_many_user(email, limit, offset)


@router.get("/api/user/{user_id}", tags=["user"], response_model=SingleResponse)
async def get_user_by_id(user_id: str) -> SingleResponse:
    return get_one_user(user_id)

@router.get("/api/user/{user_id}/organisations", tags=["user"], response_model=ListResponse)
async def get_organisation_users(user_id: str, limit: int = 10, offset: int = 0) -> ListResponse:
    return get_organisations_by_user_id(user_id, limit, offset)
