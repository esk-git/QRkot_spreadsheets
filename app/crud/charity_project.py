from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        db_charity_project_id = db_charity_project_id.scalars().first()
        return db_charity_project_id

    async def get_charity_project_by_id(
        self,
        charity_project_id: int,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_charity_project = await session.execute(
            select(CharityProject).where(CharityProject.id == charity_project_id)
        )
        db_charity_project = db_charity_project.scalars().first()
        return db_charity_project

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[CharityProject]:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).order_by(func.julianday(CharityProject.close_date) - func.julianday(CharityProject.create_date))
        )
        return projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
