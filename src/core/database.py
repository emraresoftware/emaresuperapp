"""
Emare SuperApp — Veritabanı Bağlantısı
SQLAlchemy async engine + session yönetimi.
"""
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
import pathlib

# Veritabanı dosya yolu
DATA_DIR = pathlib.Path(__file__).resolve().parent.parent.parent / "data"

# Engine (başlangıçta None, init_db ile oluşturulur)
engine = None
async_session_factory = None


class Base(DeclarativeBase):
    """Tüm modellerin temel sınıfı."""
    pass


async def init_db():
    """Veritabanını başlat ve tabloları oluştur."""
    global engine, async_session_factory

    from config.settings import get_settings
    settings = get_settings()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
        future=True,
    )

    async_session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Tabloları oluştur — modeller önceden import edilmeli
    import models  # noqa: F401 — User, Role tablolarını Base.metadata'ya kayıt eder
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Dependency injection için DB session üreteci."""
    if async_session_factory is None:
        raise RuntimeError("Veritabanı henüz başlatılmadı — init_db() çağrılmamış")
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
