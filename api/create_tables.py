from api.app.database import Base, engine
from api.app.models import Article, PipelineRun

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")