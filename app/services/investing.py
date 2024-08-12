from datetime import datetime
from typing import Union

from app.models import CharityProject, Donation


def investing_donations_in_projects(
    target: Union[CharityProject, Donation],
    sources: list[Union[CharityProject, Donation]]
) -> list[Union[CharityProject, Donation]]:
    changed_sources = []
    for source in sources:
        uninvested_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += uninvested_amount
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        changed_sources.append(source)
        if target.fully_invested:
            break
    return changed_sources
