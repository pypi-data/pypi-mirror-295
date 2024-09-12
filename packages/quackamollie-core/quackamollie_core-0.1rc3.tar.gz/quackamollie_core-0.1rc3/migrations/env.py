# -*- coding: utf-8 -*-
import alembic_postgresql_enum
import asyncio
import logging

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from typing import List, Optional, Type

from alembic import context

from quackamollie.core.cli.settings import get_settings_from_context, QuackamollieSettings

log = logging.getLogger(__name__)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the URL from the QuackamollieSettings or raise an error if not set
quackamollie_settings: Optional[QuackamollieSettings] = get_settings_from_context()
if quackamollie_settings is None:
    raise RuntimeError("Error while retrieving QuackamollieSettings from click context. Please call alembic using"
                       " 'quackamollie db alembic' and provide your database info as expected by quackamollie"
                       " (cf. `quackamollie db --help`).")
else:
    config.set_main_option("sqlalchemy.url", quackamollie_settings.db_url)

# Logging is already set by quackamollie
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
from quackamollie.core.database.meta import Base
from quackamollie.core.database.model import *
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


QUACKAMOLLIE_SCHEMA_NAMES: List[str] = ["quackamollie", "quackamollie_types"]


def include_quackamollie_schema_name(name, type_, parent_names):
    if type_ == "schema":
        # note this will not include the default schema
        return name in QUACKAMOLLIE_SCHEMA_NAMES
    else:
        return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=target_metadata.schema,
        include_schemas=True,
        include_name=include_quackamollie_schema_name,
    )

    with context.begin_transaction():
        for schema_name in QUACKAMOLLIE_SCHEMA_NAMES:
            context.execute(f'create schema if not exists {schema_name};')
        context.execute(f'set search_path to {", ".join(QUACKAMOLLIE_SCHEMA_NAMES)}')
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema=target_metadata.schema,
        include_schemas=True,
        include_name=include_quackamollie_schema_name,
    )

    with context.begin_transaction():
        for schema_name in QUACKAMOLLIE_SCHEMA_NAMES:
            context.execute(f'create schema if not exists {schema_name};')
        context.execute(f'set search_path to {", ".join(QUACKAMOLLIE_SCHEMA_NAMES)}')
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
