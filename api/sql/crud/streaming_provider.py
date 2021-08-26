from sqlalchemy.orm import Session

from .. import models
from ..schemas.streaming_provider import StreamingProviderOut, StreamingProviderCreate


def get_streaming_provider_by_name(db: Session, name: str):
    return db.query(models.StreamingProvider).filter(models.StreamingProvider.name == name).first()


def get_streaming_providers(db: Session):
    return db.query(models.StreamingProvider).all()


def create_streaming_provider(db: Session, streaming_provider: StreamingProviderCreate):

    db_streaming_provider = models.StreamingProvider(
        name=streaming_provider.name, display_priority=streaming_provider.display_priority, logo_url=streaming_provider.logo_url, tmdb_id=streaming_provider.tmdb_id)

    db.add(db_streaming_provider)
    db.commit()
    db.refresh(db_streaming_provider)

    return db_streaming_provider
