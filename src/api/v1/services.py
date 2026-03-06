"""
Emare SuperApp — Servis Gateway API
Tüm 47 Emare projesini yöneten merkezi API katmanı.

Endpoints:
  GET  /services              — tüm servis listesi
  GET  /services/{id}         — tek servis detayı
  GET  /services/health/all   — tüm servislerin sağlık durumu (paralel)
  GET  /services/{id}/health  — tek servis sağlık kontrolü
  ANY  /gateway/{id}/{path}   — şeffaf proxy
"""
from __future__ import annotations

from typing import Any, Optional
from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()


# ── Şemalar ──────────────────────────────────────────────────────────────────

class ServiceInfo(BaseModel):
    id: str
    name: str
    icon: str
    url: str
    status: str          # production | ready | development | planning
    category: str
    local_port: Optional[int] = None
    description: str
    reachable: Optional[bool] = None


class HealthResult(BaseModel):
    id: str
    name: str
    icon: str
    status: str          # healthy | offline | timeout | error | no_url | unknown
    reachable: bool
    error: Optional[str] = None
    details: Optional[dict] = None


# ── Yardımcı ─────────────────────────────────────────────────────────────────

def _get_registry() -> dict[str, dict[str, Any]]:
    from services.emare_bridge import get_service_registry
    return get_service_registry()


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get(
    "",
    summary="Tüm Emare servisleri",
    response_model=list[ServiceInfo],
)
async def list_services(
    status: Optional[str] = Query(None, description="production|ready|development|planning"),
    category: Optional[str] = Query(None, description="Kategori filtresi"),
):
    """
    Kayıt defterindeki tüm Emare servislerini döndürür.
    `status` ve `category` parametreleriyle filtreleme yapılabilir.
    """
    reg = _get_registry()
    services = list(reg.values())
    if status:
        services = [s for s in services if s.get("status") == status]
    if category:
        services = [s for s in services if s.get("category", "").lower() == category.lower()]
    return services


@router.get(
    "/health/all",
    summary="Tüm servislerin sağlık durumu (paralel)",
)
async def health_all(
    status_filter: Optional[str] = Query(None, alias="status",
                                          description="Sadece bu statüdeki servisleri kontrol et"),
):
    """
    Tüm kayıtlı servislerin `/health` endpoint'ini eş zamanlı kontrol eder.
    Production servisleri için özellikle kullanışlıdır.
    """
    from services.emare_bridge import check_all_health, get_service_registry
    reg = get_service_registry()
    if status_filter:
        ids = [sid for sid, s in reg.items() if s.get("status") == status_filter]
    else:
        ids = None  # hepsini kontrol et
    result = await check_all_health(ids)
    return result


@router.get(
    "/{service_id}",
    summary="Tek servis detayı",
    response_model=ServiceInfo,
)
async def get_service(service_id: str):
    """Belirtilen servisin kayıt bilgilerini döndürür."""
    reg = _get_registry()
    svc = reg.get(service_id)
    if not svc:
        raise HTTPException(status_code=404, detail=f"Servis bulunamadı: {service_id}")
    return svc


@router.get(
    "/{service_id}/health",
    summary="Tek servis sağlık kontrolü",
    response_model=HealthResult,
)
async def health_single(service_id: str):
    """Belirtilen servisin canlı sağlık durumunu kontrol eder."""
    from services.emare_bridge import check_service_health
    result = await check_service_health(service_id)
    if result.get("status") == "unknown":
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.api_route(
    "/gateway/{service_id}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    summary="Şeffaf proxy gateway",
    include_in_schema=True,
)
async def gateway_proxy(service_id: str, path: str, request: Request):
    """
    İsteği ilgili Emare servisine şeffaf olarak iletir.
    Tüm HTTP metodlarını destekler.

    Örnek: `GET /api/v1/services/gateway/asistan/api/stats`
    → `GET http://77.92.152.3:8000/api/stats` adresine iletilir.
    """
    from services.emare_bridge import proxy_request, get_service_registry

    reg = get_service_registry()
    if service_id not in reg:
        raise HTTPException(status_code=404, detail=f"Bilinmeyen servis: {service_id}")

    # Body'yi oku
    body: dict | None = None
    if request.method in ("POST", "PUT", "PATCH"):
        try:
            body = await request.json()
        except Exception:
            body = None

    # Query params
    params = dict(request.query_params)

    # Upstream'e gönderilecek başlıklar (Authorization ilet, Host'u temizle)
    forward_headers = {}
    if auth := request.headers.get("authorization"):
        forward_headers["Authorization"] = auth

    try:
        result = await proxy_request(
            service_id=service_id,
            method=request.method,
            path=f"/{path}",
            json=body,
            params=params or None,
            extra_headers=forward_headers or None,
        )
        return JSONResponse(content=result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"{service_id} servisinden yanıt alınamadı: {exc}",
        )
