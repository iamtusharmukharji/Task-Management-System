import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.db import DATABASE_URL  # Import your models' Base
from app.models import Base  # Replace with your actual database URL import

# Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add models' MetaData
target_metadata = Base.metadata

# Create Async Engine
connectable = create_async_engine(DATABASE_URL, future=True, echo=True)

async def run_migrations():
    """Run migrations in an asynchronous environment."""
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    """Run actual migrations."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

asyncio.run(run_migrations())
