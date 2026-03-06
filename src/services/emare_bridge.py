"""Emare Bridge — diğer Emare projelerine HTTP köprüsü.

emarecloud, emareasistan, emareflow gibi projelere tek noktadan
erişim sağlar. URL'leri ``config.settings`` üzerinden okur.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from src.core.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# HTTP istemci yapılandırması
# ---------------------------------------------------------------------------

_timeout = httpx.Timeout(timeout=30.0, connect=10.0)
_default_headers = {
    "User-Agent": "EmareSuperApp-Bridge/1.0",
    "Accept": "application/json",
}


# ---------------------------------------------------------------------------
# Genel İstek Fonksiyonu
# ---------------------------------------------------------------------------

async def _request(
    method: str,
    base_url: str,
    path: str,
    *,
    json: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Emare servisleri için genel HTTP isteği gönderir.

    Args:
        method: HTTP yöntemi (GET, POST, PUT, DELETE).
        base_url: Hedef servisin kök URL'si.
        path: Endpoint yolu.
        json: JSON body verisi.
        params: Sorgu parametreleri.
        headers: Ek HTTP başlıkları.

    Returns:
        API yanıtını içeren sözlük.
    """
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    merged_headers = {**_default_headers, **(headers or {})}

    logger.info("Bridge isteği: %s %s", method, url)

    async with httpx.AsyncClient(timeout=_timeout) as client:
        response = await client.request(
            method,
            url,
            json=json,
            params=params,
            headers=merged_headers,
        )
        response.raise_for_status()

    return response.json() if response.text else {}


# ---------------------------------------------------------------------------
# Emare Cloud
# ---------------------------------------------------------------------------

async def cloud_get(path: str, **kwargs: Any) -> dict[str, Any]:
    """EmareCloud servisinden GET isteği yapar."""
    return await _request("GET", settings.EMARE_CLOUD_URL, path, **kwargs)  # type: ignore[attr-defined]


async def cloud_post(path: str, json: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
    """EmareCloud servisine POST isteği yapar."""
    return await _request("POST", settings.EMARE_CLOUD_URL, path, json=json, **kwargs)  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Emare Asistan
# ---------------------------------------------------------------------------

async def asistan_ask(prompt: str) -> dict[str, Any]:
    """EmareAsistan servisinden AI yanıtı alır."""
    return await _request(
        "POST",
        settings.EMARE_ASISTAN_URL,  # type: ignore[attr-defined]
        "/api/ask",
        json={"prompt": prompt},
    )


# ---------------------------------------------------------------------------
# Emare Flow
# ---------------------------------------------------------------------------

async def flow_trigger(workflow_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """EmareFlow üzerinde iş akışı tetikler."""
    return await _request(
        "POST",
        settings.EMARE_FLOW_URL,  # type: ignore[attr-defined]
        f"/api/workflows/{workflow_id}/trigger",
        json=payload or {},
    )


async def flow_status(workflow_id: str, run_id: str) -> dict[str, Any]:
    """EmareFlow iş akışı çalışma durumunu sorgular."""
    return await _request(
        "GET",
        settings.EMARE_FLOW_URL,  # type: ignore[attr-defined]
        f"/api/workflows/{workflow_id}/runs/{run_id}",
    )


# ---------------------------------------------------------------------------
# Emare Database
# ---------------------------------------------------------------------------

async def database_query(query: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """EmareDatabase uzak sorgu API'sini kullanır."""
    return await _request(
        "POST",
        settings.EMARE_DATABASE_URL,  # type: ignore[attr-defined]
        "/api/query",
        json={"query": query, "params": params or {}},
    )


# ---------------------------------------------------------------------------
# Sağlık Kontrolü
# ---------------------------------------------------------------------------

async def health_check(service_name: str) -> dict[str, Any]:
    """Belirtilen Emare servisinin sağlık durumunu kontrol eder.

    Args:
        service_name: Servis adı (cloud, asistan, flow, database).

    Returns:
        Servis sağlık bilgisi.
    """
    url_map: dict[str, str] = {
        "cloud": settings.EMARE_CLOUD_URL,  # type: ignore[attr-defined]
        "asistan": settings.EMARE_ASISTAN_URL,  # type: ignore[attr-defined]
        "flow": settings.EMARE_FLOW_URL,  # type: ignore[attr-defined]
        "database": settings.EMARE_DATABASE_URL,  # type: ignore[attr-defined]
    }

    base_url = url_map.get(service_name)
    if not base_url:
        return {"service": service_name, "status": "unknown", "error": "Bilinmeyen servis"}

    try:
        result = await _request("GET", base_url, "/health")
        return {"service": service_name, "status": "healthy", "details": result}
    except Exception as exc:
        logger.warning("Sağlık kontrolü başarısız: %s — %s", service_name, exc)
        return {"service": service_name, "status": "unhealthy", "error": str(exc)}
