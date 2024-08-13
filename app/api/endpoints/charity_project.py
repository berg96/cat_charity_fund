from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists, check_charity_project_not_closed,
    check_donations_exists, check_name_duplicate,
    check_new_full_amount_more_invested_amount
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.investing import investing_donations_in_projects

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session, make_commit=False
    )
    new_charity_project.set_default()
    session.add_all(investing_donations_in_projects(
        new_charity_project,
        await donation_crud.get_not_closed_objects(session)
    ))
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB]
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(project_id, session)
    await check_donations_exists(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_not_closed(project_id, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_new_full_amount_more_invested_amount(
            project_id, obj_in.full_amount, session
        )
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    if charity_project.invested_amount == charity_project.full_amount:
        setattr(charity_project, 'fully_invested', True)
        setattr(charity_project, 'close_date', datetime.now())
        await session.commit()
        await session.refresh(charity_project)
    return charity_project
