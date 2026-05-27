from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from database import Base
from settings import settings

# IMPORTA TODOS OS MODELS AQUI
from contacts.models import ContactModel  # type: ignore
from auth.models import UserModel  # type: ignore

config = context.config

# Define DATABASE_URL dinamicamente
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL,
)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata do SQLAlchemy
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # IMPORTANTE PARA SQLITE
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # IMPORTANTE PARA SQLITE
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
