from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_not_closed_projects_exists
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate, DonationDBForUser, DonationDBFull
)
from app.services.investing import investing_donations_in_projects

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBFull],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDBForUser,
)
async def create_new_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    new_donation = await donation_crud.create(donation, session, user)
    while (
        not new_donation.fully_invested and
        await check_not_closed_projects_exists(session)
    ):
        await investing_donations_in_projects(session)
        await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDBForUser],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получает список всех пожертвований для текущего пользователя."""
    return await donation_crud.get_by_user(user, session)
