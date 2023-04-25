import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_uri = os.getenv("DB_URI")
if db_uri is None:
    raise RuntimeError("DB_URI is not defined in runtime environment")

db_engine = create_engine(db_uri)
DbSession = sessionmaker(bind=db_engine)
