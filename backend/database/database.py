"""
Database connection management with SQLAlchemy async engine.
Handles PostgreSQL connection pooling and session management.
"""
import os
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Create async engine with connection pooling
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is required!")

engine = create_async_engine(
    database_url,
    echo=False,  
    pool_pre_ping=True,  
    pool_size=10, 
    max_overflow=20, 
    pool_recycle=3600,  
    connect_args={
        "server_settings": {
            "application_name": "ai_tutor_orchestrator",
        },
        "command_timeout": 60,
        "statement_cache_size": 0,  # Disable prepared statements for pgbouncer
    }
)

# Create session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI to get database session.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize database - create all tables.
    """
    from .models import Base
    
    logger.info("Initializing database...")
    
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("✅ Database initialized successfully")
        logger.info(f"Tables created: users, conversations, chat_messages, tool_executions, parameter_extractions")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


async def close_db():
    """
    Close database connections.
    """
    logger.info("Closing database connections...")
    await engine.dispose()
    logger.info("✅ Database connections closed")


async def check_db_connection() -> bool:
    """
    Test database connection.
    Returns True if connection is successful.
    """
    try:
        from sqlalchemy import text
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False
