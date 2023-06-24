from fastapi import APIRouter
from typing import Optional
from dto.organisation import OrganisationArgs
from dto.base import SingleResponse, ListResponse
from services.organisation import create_organisation, get_many_organisation, get_one_organisation, get_users_by_org_id

router = APIRouter()


@router.post("/api/organisation/", tags=["organisation"], response_model=SingleResponse)
async def create_new_organisation(organisation: OrganisationArgs) -> SingleResponse:
    return create_organisation(organisation)


@router.get("/api/organisation/", tags=["organisation"], response_model=ListResponse)
async def get_organisations_by_filters(name: Optional[str] = None, limit: int = 10, offset: int = 0) -> ListResponse:
    return get_many_organisation(name, limit, offset)


@router.get("/api/organisation/{organisation_id}", tags=["organisation"], response_model=SingleResponse)
async def get_organisation_by_id(organisation_id: str) -> SingleResponse:
    return get_one_organisation(organisation_id)


@router.get("/api/organisation/{organisation_id}/users", tags=["organisation"], response_model=ListResponse)
async def get_organisation_users(organisation_id: str, limit: int = 10, offset: int = 0) -> ListResponse:
    return get_users_by_org_id(organisation_id, limit, offset)
