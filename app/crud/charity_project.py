from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):
    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        return (await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )).scalars().first()

    async def get_not_closed_charity_projects(
        self,
        session: AsyncSession,
    ):
        return (await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == False
            )
        )).scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
