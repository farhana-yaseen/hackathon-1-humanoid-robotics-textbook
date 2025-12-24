from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus

# Get database URL from environment variable
DATABASE_URL = os.getenv("NEON_DATABASE_URL", "postgresql+asyncpg://username:password@localhost/dbname")

# Decode special characters in DATABASE_URL if present
encoded_password = os.getenv("DB_PASSWORD", "")
if encoded_password:
    decoded_password = quote_plus(encoded_password)
    DATABASE_URL = DATABASE_URL.replace(encoded_password, decoded_password)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # Set to False in production
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()