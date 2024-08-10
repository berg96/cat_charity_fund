from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud


async def investing_donations_in_projects(
    session: AsyncSession
):
    project = (
        await charity_project_crud.get_not_closed_charity_projects(session)
    )[0]
    donation = (await donation_crud.get_not_closed_donations(session))[0]
    leftover_in_project = (project.full_amount - project.invested_amount)
    leftover_in_donation = (donation.full_amount - donation.invested_amount)
    if leftover_in_donation < leftover_in_project:
        setattr(
            project,
            'invested_amount',
            project.invested_amount + leftover_in_donation
        )
        setattr(donation, 'invested_amount', donation.full_amount)
        setattr(donation, 'fully_invested', True)
        setattr(donation, 'close_date', datetime.now())
    elif leftover_in_donation > leftover_in_project:
        setattr(project, 'invested_amount', project.full_amount)
        setattr(project, 'fully_invested', True)
        setattr(project, 'close_date', datetime.now())
        setattr(
            donation,
            'invested_amount',
            donation.invested_amount + leftover_in_project
        )
    else:
        setattr(project, 'invested_amount', project.full_amount)
        setattr(project, 'fully_invested', True)
        setattr(project, 'close_date', datetime.now())
        setattr(donation, 'invested_amount', donation.full_amount)
        setattr(donation, 'fully_invested', True)
        setattr(donation, 'close_date', datetime.now())
    await session.commit()
