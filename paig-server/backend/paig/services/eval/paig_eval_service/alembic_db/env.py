from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine
import sys, os
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
try:
    from core.config import load_config_file
except ImportError:
    PAIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
    sys.path.append(PAIG_DIR)
    config_path = os.path.join(PAIG_DIR, "conf")
    if 'CONFIG_PATH' not in os.environ:
        os.environ["CONFIG_PATH"] = str(config_path)
    sys.path.append(os.path.join(PAIG_DIR, 'services', 'paig_eval_service'))
    from core.config import load_config_file
import asyncio

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config



# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    cnf = load_config_file()
    config.set_main_option('sqlalchemy.url', cnf['database']['url'])
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
try:
    from paig_eval_service.database.db_models import eval_model, eval_targets, eval_config
except ImportError:
    from database.db_models import eval_model, eval_targets, eval_config
from core.db_session.session import Base
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


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
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
    context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
