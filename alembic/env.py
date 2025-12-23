import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 1. Import your models and settings
from app.db.models import Base
from app.core.config import settings 
DATABASE_URL = settings.DATABASE_URL  # Using the URL you defined in base.py

config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Set the target metadata for autogenerate support
target_metadata = Base.metadata

def do_run_migrations(connection):
    """
    This is the synchronous part called inside 'run_sync'.
    Alembic's migration logic lives here.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """
    Run migrations in 'online' mode using an async engine.
    """
    configuration = config.get_section(config.config_ini_section)
    # Force the async URL into the configuration
    configuration["sqlalchemy.url"] = DATABASE_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # This allows the sync Alembic code to run on the async connection
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    # Use asyncio.run to handle the async online migration flow
    asyncio.run(run_migrations_online())