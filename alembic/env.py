from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import os
import sys

# App path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# App settings
from app.core.config import settings
from app.db.base import Base  # model metadata

# Alembic config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# DB URL (async)
config.set_main_option("sqlalchemy.url", settings.db_url)

# metadata
target_metadata = Base.metadata


def run_migrations_offline():
    """Offline migration"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Sync-style function to pass into run_sync"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Online migration with async engine"""
    connectable = create_async_engine(
        settings.db_url,
        poolclass=pool.NullPool,
    )

    async def async_main():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    import asyncio
    asyncio.run(async_main())


# Migration runner
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
