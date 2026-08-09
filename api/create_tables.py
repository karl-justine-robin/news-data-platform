from src.database.database import Base, engine
from src.database.models import (
    Article,
    PipelineRun,
    DimDate,
    DimSource,
    DimCategory,
    FactArticle,
)


Base.metadata.create_all(
    bind=engine
)


print(
    "Database tables created successfully."
)