from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .utils import creds


DATABASE_URL = f"postgresql+asyncpg://{creds.database['username']}:{creds.database['password']}@localhost/{creds.database['schema']}"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(engine, class_ = AsyncSession, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session
