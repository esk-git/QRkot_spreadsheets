from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_before_delete,
                                check_charity_project_close_before_edit,
                                check_charity_project_exists,
                                check_full_amount_before_edit,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.invest import invest_funds

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    await invest_funds(new_charity_project, session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session),
):
    charity_project_all = await charity_project_crud.get_multi(session)
    return charity_project_all


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_poject(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(charity_project_id, session)
    await check_charity_project_close_before_edit(charity_project_id, session)
    if obj_in.full_amount is not None:
        await check_full_amount_before_edit(
            charity_project_id, obj_in.full_amount, session
        )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    charity_project = await charity_project_crud.update(charity_project, obj_in, session)
    await invest_funds(charity_project, session)
    await session.refresh(charity_project)
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    charity_project = await check_charity_project_before_delete(
        charity_project_id, session
    )
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
