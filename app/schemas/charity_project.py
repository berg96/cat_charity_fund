from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

NULL_NAME = 'Название проекта не может быть пустым!'
NULL_DESCRIPTION = 'Описание проекта не может быть пустым!'
NULL_FULL_AMOUNT = 'Цель проекта не может быть пустым!'


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError(NULL_NAME)
        return value

    @validator('description')
    def description_cannot_be_null(cls, value):
        if value is None:
            raise ValueError(NULL_DESCRIPTION)
        return value

    @validator('full_amount')
    def full_amount_cannot_be_null(cls, value):
        if value is None:
            raise ValueError(NULL_FULL_AMOUNT)
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
