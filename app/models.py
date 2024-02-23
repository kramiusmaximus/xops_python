from db import Base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
)


class DomainItem(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True)
    domain = Column(String)
    date_visited = Column(
        DateTime, index=True
    )  # Индекс для быстрого поиска промежутков


Base.metadata.create_all(Base.metadata.bind)
