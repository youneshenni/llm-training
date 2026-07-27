from sqlalchemy import create_engine
from db.models import Base

engine = create_engine("sqlite:///example.db", echo=True)
Base.metadata.create_all(engine)