from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationAll
from app.services.invest import invest_funds


router = APIRouter()


@router.post("/", response_model=DonationDB, response_model_exclude_none=True)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    await invest_funds(new_donation, session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    "/",
    dependencies=[Depends(current_superuser)],
    response_model=List[DonationAll],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get("/my", response_model=List[DonationDB])
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donations = await donation_crud.get_donation_by_user(session=session, user=user)
    return donations
