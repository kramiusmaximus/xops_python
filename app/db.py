from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_URL


engine = create_engine(DB_URL)

Base = declarative_base()
Base.metadata.bind = engine

SessionLocal = sessionmaker(autoflush=True, bind=engine)


def get_db():
    with SessionLocal.begin() as session:
        yield session
