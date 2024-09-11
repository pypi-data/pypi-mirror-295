import time
import uuid

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class JobRecord(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    runtime = Column(String, nullable=False)
    namespace = Column(String, nullable=True)
    phase = Column(String, nullable=True)
    logs = Column(String, nullable=True)
    pid = Column(Integer, nullable=True)
    result = Column(String, nullable=True)
    created = Column(Float, default=time.time)
    updated = Column(Float, default=time.time)
    finished = Column(Float, default=0.0)
    metadata_ = Column(String, nullable=True)
