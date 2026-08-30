import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Conexão com BD
engine = create_async_engine(
    DATABASE_URL,
    echo = False,
    pool_pre_ping = True
)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base
Base = declarative_base()

# Session

async def getSession():
    async with AsyncSessionLocal() as session:
        yield session