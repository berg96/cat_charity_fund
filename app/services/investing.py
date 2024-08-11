from datetime import datetime


def investing_donations_in_projects(target, sources):
    changed_sources = []
    for source in sources:
        min_uninvested_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += min_uninvested_amount
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
                if obj is source:
                    changed_sources.append(obj)
        if target.fully_invested:
            break
    return changed_sources
