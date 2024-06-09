from sqlalchemy.orm import DeclarativeBase

from gebwai.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
