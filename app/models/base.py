from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class CharityBaseModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            name='check_invested_amount_non_negative_and_less_full_amount'
        ),
    )

    def __repr__(self):
        return (
            f'{type(self).__name__} '
            f'{self.invested_amount}/{self.full_amount} '
            f'{self.create_date} // {self.close_date}'
        )

    def set_default(self):
        self.invested_amount = 0
        self.fully_invested = False
        self.create_date = datetime.now()
