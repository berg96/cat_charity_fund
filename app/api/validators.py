from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject

NAME_DUPLICATE = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден!'
PROJECT_IS_CLOSED = 'Проект закрыт и недоступен для редактирования!'
PROJECT_HAS_DONATIONS = 'В проект были внесены средства, не подлежит удалению!'
FULL_AMOUNT_LESS_INVESTED_AMOUNT = (
    'Нельзя установить значение full_amount '
    'меньше уже вложенной суммы.'
)


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    if await charity_project_crud.get_project_id_by_name(
        project_name, session
    ):
        raise HTTPException(
            status_code=400,
            detail=NAME_DUPLICATE,
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail=PROJECT_NOT_FOUND
        )
    return charity_project


async def check_charity_project_not_closed(
    project_id: int,
    session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail=PROJECT_IS_CLOSED
        )


async def check_donations_exists(
    project_id: int,
    session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail=PROJECT_HAS_DONATIONS
        )


async def check_new_full_amount_more_invested_amount(
    project_id: int,
    new_full_amount: int,
    session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if new_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail=FULL_AMOUNT_LESS_INVESTED_AMOUNT
        )
