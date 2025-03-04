from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

dbUserName = "postgres"
dbPassword = "admin"
dbName = "test"

DATABASE_URL = f"postgresql+asyncpg://{dbUserName}:{dbPassword}@localhost/{dbName}"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session
