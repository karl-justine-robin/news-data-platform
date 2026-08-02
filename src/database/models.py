from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)

from src.database.database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(Text, nullable=False)
    published_at = Column(Date, nullable=False)
    body = Column(Text, nullable=False)
    source = Column(String(100), nullable=False)
    loaded_at = Column(DateTime, nullable=False)


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id = Column(Integer, primary_key=True, index=True)

    pipeline_name = Column(String(100))
    status = Column(String(50))

    start_time = Column(DateTime)
    end_time = Column(DateTime)

    duration_seconds = Column(Float)

    records_processed = Column(Integer)

    error_message = Column(Text)