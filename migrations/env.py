"""
Emare SuperApp — Alembic Migration Ortamı
Async SQLAlchemy + Pydantic Settings entegrasyonu.
"""
import asyncio
import sys
import os
from logging.config import fileConfig

from sqlalchemy import pool, create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# src yolunu ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Ayarları yükle
from config.settings import get_settings  # noqa: E402

settings = get_settings()

# Alembic Config nesnesi
config = context.config

# .ini log ayarlarını yapılandır
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Database URL'yi settings'ten al (sync driver ile)
_db_url = settings.database_url
_db_url = _db_url.replace("sqlite+aiosqlite", "sqlite")
_db_url = _db_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
config.set_main_option("sqlalchemy.url", _db_url)

# Model metadata — autogenerate için
from core.database import Base      # noqa: E402
from models import user, wallet, product, notification  # noqa: F401, E402

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Offline modda migration — DB bağlantısı gerekmez."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online modda migration — sync engine kullanır."""
    url = config.get_main_option("sqlalchemy.url")
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

