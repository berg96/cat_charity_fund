from sqlalchemy import Column, String, Text

from app.models.base import CharityBaseModel


class CharityProject(CharityBaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'{self.name} {super().__repr__()}'
