from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import CharityBaseModel


class Donation(CharityBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return f'{self.user_id} {super().__repr__()}'
