from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from util.settings import get_settings


def get_state_db():
    db = AppStateSession()
    try:
        yield db
    finally:
        db.close()


BaseSqlModel = declarative_base()

app_state_engine = create_engine(
    get_settings().app_state_sqlite_url, connect_args={"check_same_thread": False}
)
AppStateSession = sessionmaker(autocommit=False, autoflush=False, bind=app_state_engine)
