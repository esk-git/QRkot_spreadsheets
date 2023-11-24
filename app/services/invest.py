from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_funds(
    investment_object: Union[CharityProject, Donation],
    session: AsyncSession
) -> Union[CharityProject, Donation]:
    invested_model = (
        CharityProject if isinstance(investment_object, Donation) else Donation
    )
    not_invested_objects = await get_not_fully_invested_objects(
        invested_model, session
    )

    if not_invested_objects:
        remaining_amount = investment_object.full_amount
        for obj in not_invested_objects:
            required_amount = obj.full_amount - obj.invested_amount
            investment = (
                required_amount
                if required_amount < remaining_amount
                else remaining_amount
            )
            remaining_amount -= investment
            obj.invested_amount += investment
            investment_object.invested_amount += investment

            if obj.full_amount == obj.invested_amount:
                await close_invested_object(obj)

            if not remaining_amount:
                await close_invested_object(investment_object)
                break
        await session.commit()
    return investment_object


async def get_not_fully_invested_objects(
    model: Union[CharityProject, Donation], session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    objects = await session.execute(
        select(model)
        .where(model.fully_invested == False)  # noqa
        .order_by(model.create_date)
    )
    return objects.scalars().all()


async def close_invested_object(
        obj_to_close: Union[CharityProject, Donation],
) -> None:
    obj_to_close.fully_invested = True
    obj_to_close.close_date = datetime.now()
