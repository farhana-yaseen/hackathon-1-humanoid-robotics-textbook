"""
SQLAlchemy Database Model for Module Access Log
"""
from sqlalchemy import Column, String, DateTime, Integer, UUID, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class ModuleAccessLogDB(Base):
    __tablename__ = "module_access_log"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(String(255), nullable=False)
    module_id = Column(String(255), nullable=False)
    access_time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    session_id = Column(String(255), nullable=True)
    position = Column(Integer, default=0, nullable=True)