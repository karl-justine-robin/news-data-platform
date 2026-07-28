from sqlalchemy import Column, Date, DateTime, Integer, String, Text

from app.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(Text, nullable=False)
    published_at = Column(Date, nullable=False)
    body = Column(Text, nullable=False)
    source = Column(String(100), nullable=False)
    loaded_at = Column(DateTime, nullable=False)