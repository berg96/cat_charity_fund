from datetime import datetime

from app.models import CharityBaseModel


def investing_donations_in_projects(
    target: CharityBaseModel,
    sources: list[CharityBaseModel]
) -> list[CharityBaseModel]:
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
