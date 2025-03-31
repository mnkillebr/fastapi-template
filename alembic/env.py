import os, re, sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool


# # Add the backend folder to sys.path so that we can import app modules.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import the metadata from your models.
from sqlmodel import SQLModel
# Ensure that all models are imported so that metadata is populated.
from app.models import user  # Import your user model. Import additional models as needed.
from app.core.config import settings

target_metadata = SQLModel.metadata


def get_url():
    db_url = str(settings.DATABASE_URL)
    if settings.ALEMBIC_LOCAL == "1":
        # Replace the internal Docker hostname 'db' with 'localhost', replace port '5432' with '5433' and remove '+asyncpg' for synchronous migrations.
        db_url = re.sub(r"@db:", "@localhost:", db_url)
        db_url = re.sub(r"\+asyncpg", "", db_url)
        db_url = re.sub(r":5432", ":5433", db_url)
    return db_url


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        # compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario, we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # comare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

