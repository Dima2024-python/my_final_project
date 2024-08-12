from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, Sequence, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import config

Base = declarative_base()


class Travel(Base):
    __tablename__ = "Travels"

    id = Column(Integer, Sequence("travel_id_seq"), primary_key=True)
    country = Column(String, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False, default=100.0)
    hotel_class = Column(Integer, nullable=False)
    image = Column(String, default="")
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


engine = create_engine(config.DB_PATH, echo=config.DEBUG)

Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    Base.metadata.create_all(engine)