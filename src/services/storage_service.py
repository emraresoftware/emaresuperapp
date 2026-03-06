"""Storage Service — dosya depolama servisi (yerel + S3 uyumlu)."""

from __future__ import annotations

import hashlib
import logging
import os
import shutil
from pathlib import Path
from typing import Any
from uuid import uuid4

from src.core.config import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Yerel Depolama
# ---------------------------------------------------------------------------

class LocalStorage:
    """Yerel dosya sistemi üzerinde depolama."""

    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = Path(base_dir or getattr(settings, "STORAGE_LOCAL_DIR", "./storage"))
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def upload(
        self,
        content: bytes,
        filename: str | None = None,
        folder: str = "",
    ) -> dict[str, Any]:
        """Dosyayı yerel diske kaydeder.

        Args:
            content: Dosya içeriği (bayt).
            filename: Dosya adı; verilmezse UUID üretilir.
            folder: Alt klasör yolu.

        Returns:
            Kaydedilen dosya bilgileri.
        """
        file_id = str(uuid4())
        if not filename:
            filename = file_id

        target_dir = self.base_dir / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path = target_dir / filename

        file_path.write_bytes(content)

        checksum = hashlib.sha256(content).hexdigest()
        logger.info("Dosya kaydedildi: %s (%d bayt)", file_path, len(content))

        return {
            "id": file_id,
            "filename": filename,
            "path": str(file_path),
            "size": len(content),
            "checksum": checksum,
        }

    async def download(self, file_path: str) -> bytes | None:
        """Yerel diskten dosya okur.

        Returns:
            Dosya içeriği veya ``None``.
        """
        path = Path(file_path)
        if not path.exists():
            logger.warning("Dosya bulunamadı: %s", file_path)
            return None
        return path.read_bytes()

    async def delete(self, file_path: str) -> bool:
        """Yerel diskten dosya siler.

        Returns:
            Başarılıysa ``True``.
        """
        path = Path(file_path)
        if path.exists():
            path.unlink()
            logger.info("Dosya silindi: %s", file_path)
            return True
        return False

    async def list_files(self, folder: str = "") -> list[dict[str, Any]]:
        """Yerel klasördeki dosyaları listeler."""
        target_dir = self.base_dir / folder
        if not target_dir.exists():
            return []

        return [
            {
                "filename": f.name,
                "path": str(f),
                "size": f.stat().st_size,
            }
            for f in target_dir.iterdir()
            if f.is_file()
        ]


# ---------------------------------------------------------------------------
# S3 Uyumlu Depolama
# ---------------------------------------------------------------------------

class S3Storage:
    """S3-uyumlu nesne depolama (MinIO, AWS S3, DigitalOcean Spaces, vb.)."""

    def __init__(self) -> None:
        # TODO: boto3 / aioboto3 istemcisini yapılandır
        self.bucket = getattr(settings, "S3_BUCKET", "emare-superapp")
        self.endpoint = getattr(settings, "S3_ENDPOINT", None)
        self.region = getattr(settings, "S3_REGION", "eu-west-1")

    async def upload(
        self,
        content: bytes,
        key: str,
        content_type: str = "application/octet-stream",
    ) -> dict[str, Any]:
        """S3'e dosya yükler.

        Args:
            content: Dosya içeriği.
            key: S3 nesne anahtarı.
            content_type: MIME tipi.

        Returns:
            Yükleme sonuç bilgileri.
        """
        # TODO: aioboto3 ile asenkron yükleme
        logger.info("S3 yükleme: bucket=%s key=%s boyut=%d", self.bucket, key, len(content))
        return {
            "bucket": self.bucket,
            "key": key,
            "size": len(content),
            "content_type": content_type,
        }

    async def download(self, key: str) -> bytes | None:
        """S3'ten dosya indirir."""
        # TODO: aioboto3 ile asenkron indirme
        logger.warning("S3 indirme henüz uygulanmadı: %s", key)
        return None

    async def delete(self, key: str) -> bool:
        """S3'ten dosya siler."""
        # TODO: aioboto3 ile asenkron silme
        logger.warning("S3 silme henüz uygulanmadı: %s", key)
        return False

    async def get_presigned_url(self, key: str, expires_in: int = 3600) -> str | None:
        """Geçici erişim URL'si oluşturur.

        Args:
            key: S3 nesne anahtarı.
            expires_in: URL geçerlilik süresi (saniye).

        Returns:
            Ön-imzalı URL veya ``None``.
        """
        # TODO: aioboto3 ile presigned URL oluştur
        return None


# ---------------------------------------------------------------------------
# Fabrika — aktif depolama sağlayıcısını döndürür
# ---------------------------------------------------------------------------

def get_storage(provider: str = "local") -> LocalStorage | S3Storage:
    """Yapılandırmaya göre depolama sağlayıcısı döndürür.

    Args:
        provider: ``"local"`` veya ``"s3"``.
    """
    if provider == "s3":
        return S3Storage()
    return LocalStorage()
