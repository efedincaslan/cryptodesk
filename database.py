import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

load_dotenv()
user = os.getenv("dbusername")
password = os.getenv('dbpassword')

conn_str = f"postgresql+asyncpg://{user}:{password}@localhost:5432/cryptodesk"

engine = create_async_engine(conn_str, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    
    async with async_session() as session:
        yield session
    