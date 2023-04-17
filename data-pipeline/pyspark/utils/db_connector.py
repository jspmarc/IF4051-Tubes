import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_uri = os.getenv("DB_URI")
if db_uri is None:
    exit(1)

db_engine = create_engine(db_uri)
DbSession = sessionmaker(bind=db_engine)
