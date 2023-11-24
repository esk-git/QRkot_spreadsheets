from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.constants import MAX_LENGHT, MIN_LENGHT


class CharityProjectBase(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=MAX_LENGHT
    )
    description: str = Field(..., min_length=MIN_LENGHT)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(
        None, min_length=1, max_length=MAX_LENGHT
    )
    description: Optional[str] = Field(None, min_length=MIN_LENGHT)
    full_amount: Optional[PositiveInt]
