from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation
from app.schemas.donation import DonationCreate, DonationUpdate


class CRUDDonation(CRUDBase[
    Donation,
    DonationCreate,
    DonationUpdate
]):
    async def get_by_user(
            self,
            user: int,
            session: AsyncSession,
    ):
        return (
            await session.execute(select(Donation).where(
                Donation.user_id == user.id
            ))
        ).scalars().all()


donation_crud = CRUDDonation(Donation)
