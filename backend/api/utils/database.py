"""
Database utilities for SQLAlchemy async sessions
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
import urllib.parse

# Get database URL from environment
DATABASE_URL = os.getenv("NEON_DATABASE_URL")

if DATABASE_URL:
    # Parse the URL to extract components and handle SSL properly
    parsed = urllib.parse.urlparse(DATABASE_URL)

    # Extract components
    scheme = parsed.scheme
    username = parsed.username
    password = parsed.password
    hostname = parsed.hostname
    port = parsed.port
    database = parsed.path.lstrip('/')

    # Get query parameters
    query_params = urllib.parse.parse_qs(parsed.query)

    # Build a new URL without problematic parameters for asyncpg
    # asyncpg handles SSL differently than psycopg2
    password_encoded = urllib.parse.quote_plus(password) if password else ''
    hostname_port = f"{hostname}:{port}" if port else hostname

    # Create the new URL with asyncpg scheme but without problematic SSL parameters
    # asyncpg handles SSL automatically when connecting to Neon
    DATABASE_URL = f"postgresql+asyncpg://{username}:{password_encoded}@{hostname_port}/{database}"

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections after 5 minutes
    # Additional asyncpg-specific parameters if needed
    connect_args={
        # These parameters may help with Neon connection
        "server_settings": {
            "application_name": "humanoid-robotics-textbook",
        }
    } if hasattr(create_async_engine, 'connect_args') else {}
)

# Create async session factory
AsyncSessionFactory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncSession:
    """
    Dependency to provide async database sessions.
    Use this for SQLAlchemy-based repositories.
    """
    async with AsyncSessionFactory() as session:
        yield session