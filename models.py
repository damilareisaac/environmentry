from sqlalchemy import Boolean, Column, Integer, Float, String, DateTime

from config import Base


class Metric(Base):
    __tablename__ = "metric"
    id = Column(Integer, primary_key=True)
    variable = Column(String(128))
    units = Column(String(32))
    sensor_name = Column(String(128))
    value = Column(Float)
    is_flagged = Column(Boolean())
    timestamp = Column(DateTime())
