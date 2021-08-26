from sqlalchemy.orm import Session

from .. import models
from ..schemas.release_period import ReleasePeriodCreate


def get_release_period_by_name(db: Session, name: str):
    return db.query(models.ReleasePeriod).filter(models.ReleasePeriod.name == name).first()


def get_release_period_by_year(db: Session, year: int):
    periods = db.query(models.ReleasePeriod).all()

    for period in periods:
        if period.lower_bound <= year <= period.upper_bound:
            return period


def get_release_periods(db: Session):
    return db.query(models.ReleasePeriod).all()


def create_release_period(db: Session, release_period: ReleasePeriodCreate):

    # release date: 2002-12-13
    db_release_period = models.ReleasePeriod(
        name=release_period.name, lower_bound=release_period.lower_bound, upper_bound=release_period.upper_bound)

    db.add(db_release_period)
    db.commit()
    db.refresh(db_release_period)

    return release_period
