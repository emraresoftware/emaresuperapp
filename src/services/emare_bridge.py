"""
Emare Bridge — 47 Emare projesine tek noktadan HTTP köprüsü.

Her Emare servisi için:
  - Tip güvenlikli helper fonksiyonlar
  - Paralel sağlık kontrolü
  - Şeffaf proxy desteği (gateway)

Kullanım:
    from services.emare_bridge import asistan_ask, cloud_get, SERVICE_REGISTRY
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_timeout = httpx.Timeout(timeout=30.0, connect=5.0)
_HEADERS = {"User-Agent": "EmareSuperApp-Bridge/2.0", "Accept": "application/json"}

# ════════════════════════════════════════════════════════════════════════════════
# Servis Kayıt Defteri — tüm Emare projeleri
# ════════════════════════════════════════════════════════════════════════════════

def _registry() -> dict[str, dict[str, Any]]:
    """Settings'ten dinamik olarak okunan servis kayıt defteri."""
    from config.settings import get_settings
    s = get_settings()
    return {
        # ── PRODUCTION ────────────────────────────────────────────────────
        "asistan": {
            "id": "asistan", "name": "Emare Asistan", "icon": "🤖",
            "url": s.emare_asistan_url, "status": "production",
            "category": "SaaS Platform", "local_port": 8000,
            "description": "WhatsApp/TG/IG AI müşteri hizmetleri",
        },
        "cloud": {
            "id": "cloud", "name": "EmareCloud", "icon": "☁️",
            "url": s.emare_cloud_url, "status": "production",
            "category": "Infrastructure", "local_port": 5555,
            "domain": "emarecloud.tr",
            "health_path": "/health",
            "tech": "Flask + SocketIO + Gunicorn + Nginx",
            "description": "Multi-tenant altyapı yönetim paneli — SSH, LXD, firewall, marketplace, Cloudflare",
        },
        "finance": {
            "id": "finance", "name": "Emare Finance", "icon": "💰",
            "url": s.emare_finance_url, "status": "production",
            "category": "SaaS Platform", "local_port": 3000,
            "description": "SaaS POS + e-Fatura + AI asistan (Laravel 12)",
        },
        "makale": {
            "id": "makale", "name": "Emare Makale", "icon": "📝",
            "url": s.emare_makale_url, "status": "production",
            "category": "Tool", "local_port": 5000,
            "description": "Otomatik TR makale üretimi (GPT-4o)",
        },
        "team": {
            "id": "team", "name": "Emare Team", "icon": "🏢",
            "url": s.emare_team_url, "status": "production",
            "category": "Tool", "local_port": 5001,
            "description": "Kanban + görev yönetimi",
        },
        "dashboard": {
            "id": "dashboard", "name": "Emare Dashboard", "icon": "📊",
            "url": s.emare_dashboard_url, "status": "production",
            "category": "Infrastructure", "local_port": 5050,
            "description": "Ekosistem kontrol paneli",
        },
        "code": {
            "id": "code", "name": "Emare Code", "icon": "💻",
            "url": s.emare_code_url, "status": "production",
            "category": "Tool", "local_port": 8010,
            "description": "Cross-platform AI kod üretici (Gemini/OpenAI)",
        },
        # ── READY ─────────────────────────────────────────────────────────
        "desk": {
            "id": "desk", "name": "EmareDesk", "icon": "🖥️",
            "url": s.emare_desk_url, "status": "ready",
            "category": "Tool", "local_port": 8765,
            "description": "WebSocket uzak masaüstü — RemoteView v2",
        },
        "hive": {
            "id": "hive", "name": "Hive Coordinator", "icon": "👥",
            "url": s.emare_hive_url, "status": "ready",
            "category": "Infrastructure", "local_port": 8001,
            "description": "9B düğümlü yazılım ekibi koordinasyonu",
        },
        "katip": {
            "id": "katip", "name": "Emare Katip", "icon": "📋",
            "url": s.emare_katip_url, "status": "ready",
            "category": "Tool", "local_port": 8020,
            "description": "Proje tarayıcı + raporlayıcı",
        },
        "github": {
            "id": "github", "name": "Emare GitHub", "icon": "🐙",
            "url": s.emare_github_url, "status": "ready",
            "category": "Tool", "local_port": 8030,
            "description": "Toplu GitHub push — 27 proje",
        },
        # ── DEVELOPMENT ───────────────────────────────────────────────────
        "pos": {
            "id": "pos", "name": "Emare POS", "icon": "🍽️",
            "url": s.emare_pos_url, "status": "development",
            "category": "POS", "local_port": 8082,
            "description": "Restoran/kafe adisyon sistemi (Laravel 12)",
        },
        "log": {
            "id": "log", "name": "Emare Log", "icon": "📡",
            "url": s.emare_log_url, "status": "development",
            "category": "SaaS Platform", "local_port": 8083,
            "description": "ISS CRM+ERP+NOC — MikroTik, 5651 log",
        },
        "aplincedesk": {
            "id": "aplincedesk", "name": "Emare Aplince Desk", "icon": "🔧",
            "url": s.emare_aplincedesk_url, "status": "development",
            "category": "SaaS Platform", "local_port": 8084,
            "description": "Teknik servis + cihaz onarım yönetimi",
        },
        "cc": {
            "id": "cc", "name": "Emare CC", "icon": "☎️",
            "url": s.emare_cc_url, "status": "development",
            "category": "SaaS Platform", "local_port": 3080,
            "description": "Çağrı merkezi — Asterisk, AI transkript",
        },
        "setup": {
            "id": "setup", "name": "EmareSetup", "icon": "🏭",
            "url": s.emare_setup_url, "status": "development",
            "category": "Infrastructure", "local_port": 8000,
            "description": "AI yazılım fabrikası CLI (React 19 + Gemini)",
        },
        "hup": {
            "id": "hup", "name": "EmareHup", "icon": "🧠",
            "url": s.emare_hup_url, "status": "development",
            "category": "Infrastructure", "local_port": 5555,
            "description": "DevM otonom geliştirme orchestrator",
        },
        "flow": {
            "id": "flow", "name": "Emare Flow", "icon": "🔄",
            "url": s.emare_flow_url, "status": "development",
            "category": "Automation", "local_port": 5173,
            "description": "n8n benzeri görsel iş akışı (React Flow)",
        },
        "intranet": {
            "id": "intranet", "name": "Emare Intranet", "icon": "🌶️",
            "url": s.emare_intranet_url, "status": "development",
            "category": "Platform", "local_port": 8200,
            "description": "İç iletişim platformu (Flask + Bootstrap 5)",
        },
        "crypto": {
            "id": "crypto", "name": "Emare Crypto", "icon": "⚡",
            "url": s.emare_crypto_url, "status": "development",
            "category": "Platform", "local_port": 8300,
            "description": "Kripto/blockchain entegrasyonu",
        },
        "pazar": {
            "id": "pazar", "name": "Emare Pazar", "icon": "🚀",
            "url": s.emare_pazar_url, "status": "development",
            "category": "SaaS Platform", "local_port": 8500,
            "description": "Ürün/hizmet pazaryeri",
        },
        "aimusic": {
            "id": "aimusic", "name": "Emare AI Music", "icon": "🎵",
            "url": s.emare_aimusic_url, "status": "development",
            "category": "Platform", "local_port": 8700,
            "description": "AI müzik üretim servisi",
        },
        "webdizayn": {
            "id": "webdizayn", "name": "Emare Webdizayn", "icon": "🎨",
            "url": s.emare_webdizayn_url, "status": "development",
            "category": "Platform", "local_port": 8900,
            "description": "UI/UX + dijital ajans yönetimi",
        },
        "ai": {
            "id": "ai", "name": "Emare AI", "icon": "🤖",
            "url": s.emare_ai_url, "status": "development",
            "category": "Core Engine", "local_port": 8888,
            "description": "Self-hosted LLM — LLaMA/Mistral fine-tuning",
        },
        "vscodeasistan": {
            "id": "vscodeasistan", "name": "Emare VS Code Asistan", "icon": "🔄",
            "url": s.emare_vscodeasistan_url, "status": "development",
            "category": "Tool", "local_port": 8040,
            "description": "VS Code/Cursor ayar senkronizasyonu",
        },
        "ads": {
            "id": "ads", "name": "Emare Ads", "icon": "📢",
            "url": s.emare_ads_url, "status": "development",
            "category": "Tool", "local_port": 8050,
            "description": "AI-powered browser extension backend",
        },
        "ulak": {
            "id": "ulak", "name": "Emare Ulak", "icon": "🔌",
            "url": s.emare_ulak_url, "status": "development",
            "category": "Tool", "local_port": 8060,
            "description": "Chat izleyici + WebSocket analiz",
        },
        "siber": {
            "id": "siber", "name": "SiberEmare", "icon": "🛡️",
            "url": s.emare_siberemare_url, "status": "development",
            "category": "Security", "local_port": 8120,
            "description": "Multi-agent pentest rapor pipeline",
        },
        "oracle": {
            "id": "oracle", "name": "ZeusDB / EmareOracle", "icon": "🗄️",
            "url": s.emare_oracle_url, "status": "development",
            "category": "Core Engine", "local_port": 7777,
            "description": "C11'de yazılmış ACID veritabanı motoru",
        },
        "hosting": {
            "id": "hosting", "name": "Emare Hosting", "icon": "🌐",
            "url": s.emare_hosting_url, "status": "development",
            "category": "Infrastructure", "local_port": 8110,
            "description": "Hosting altyapısı",
        },
        "superapp": {
            "id": "superapp", "name": "Emare SuperApp", "icon": "🚀",
            "url": f"http://localhost:{s.port}", "status": "development",
            "category": "Platform", "local_port": s.port,
            "description": "Tüm Emare hizmetlerini birleştiren süper uygulama",
        },
    }


# Kolayca erişilebilen global referans
SERVICE_REGISTRY: dict[str, dict[str, Any]] = {}


def get_service_registry() -> dict[str, dict[str, Any]]:
    """Güncel servis kaydını döndürür."""
    return _registry()


# ════════════════════════════════════════════════════════════════════════════════
# Çekirdek HTTP istemcisi
# ════════════════════════════════════════════════════════════════════════════════

async def _request(
    method: str,
    base_url: str,
    path: str,
    *,
    json: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Emare servisleri için genel HTTP isteği gönderir."""
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    merged = {**_HEADERS, **(headers or {})}
    t = httpx.Timeout(timeout=timeout, connect=5.0)
    async with httpx.AsyncClient(timeout=t) as client:
        resp = await client.request(method, url, json=json, params=params, headers=merged)
        resp.raise_for_status()
    return resp.json() if resp.text else {}


# ════════════════════════════════════════════════════════════════════════════════
# Sağlık Kontrolleri
# ════════════════════════════════════════════════════════════════════════════════

async def check_service_health(service_id: str) -> dict[str, Any]:
    """Tek bir servisin sağlık durumunu kontrol eder."""
    reg = _registry()
    svc = reg.get(service_id)
    if not svc:
        return {"id": service_id, "status": "unknown", "error": "Kayıtlı servis değil"}
    if not svc.get("url"):
        return {"id": service_id, "name": svc["name"], "status": "no_url", "reachable": False}

    try:
        health_path = svc.get("health_path", "/health")
        result = await _request("GET", svc["url"], health_path, timeout=5.0)
        return {
            "id": service_id, "name": svc["name"], "icon": svc["icon"],
            "status": "healthy", "reachable": True, "details": result,
        }
    except httpx.ConnectError:
        return {"id": service_id, "name": svc["name"], "icon": svc["icon"],
                "status": "offline", "reachable": False, "error": "Bağlantı reddedildi"}
    except httpx.TimeoutException:
        return {"id": service_id, "name": svc["name"], "icon": svc["icon"],
                "status": "timeout", "reachable": False, "error": "Zaman aşımı"}
    except Exception as exc:
        return {"id": service_id, "name": svc["name"], "icon": svc["icon"],
                "status": "error", "reachable": False, "error": str(exc)}


async def check_all_health(service_ids: list[str] | None = None) -> dict[str, Any]:
    """Tüm servislerin (veya istenenlerin) sağlığını paralel kontrol eder."""
    reg = _registry()
    ids = service_ids or list(reg.keys())
    results = await asyncio.gather(*[check_service_health(sid) for sid in ids])
    healthy = sum(1 for r in results if r.get("reachable"))
    return {
        "total": len(results),
        "healthy": healthy,
        "offline": len(results) - healthy,
        "services": {r["id"]: r for r in results},
    }


# ════════════════════════════════════════════════════════════════════════════════
# Şeffaf Proxy (Gateway)
# ════════════════════════════════════════════════════════════════════════════════

async def proxy_request(
    service_id: str,
    method: str,
    path: str,
    json: dict | None = None,
    params: dict | None = None,
    extra_headers: dict | None = None,
) -> dict[str, Any]:
    """Belirtilen servise şeffaf proxy isteği gönderir."""
    reg = _registry()
    svc = reg.get(service_id)
    if not svc:
        raise ValueError(f"Bilinmeyen servis: {service_id}")
    if not svc.get("url"):
        raise ValueError(f"'{service_id}' servisinin URL'si tanımlı değil")
    return await _request(method, svc["url"], path, json=json, params=params, headers=extra_headers)


# ════════════════════════════════════════════════════════════════════════════════
# Servis-Özel Yardımcılar
# ════════════════════════════════════════════════════════════════════════════════

async def asistan_ask(prompt: str, tenant_id: str = "default") -> dict[str, Any]:
    """Emare Asistan'a AI sorusu gönderir."""
    from config.settings import get_settings
    return await _request("POST", get_settings().emare_asistan_url, "/api/ask",
                          json={"prompt": prompt, "tenant_id": tenant_id})


async def cloud_get(path: str, **kwargs: Any) -> dict[str, Any]:
    """EmareCloud'dan GET isteği."""
    from config.settings import get_settings
    return await _request("GET", get_settings().emare_cloud_url, path, **kwargs)


async def cloud_post(path: str, json: dict | None = None, **kwargs: Any) -> dict[str, Any]:
    """EmareCloud'a POST isteği."""
    from config.settings import get_settings
    return await _request("POST", get_settings().emare_cloud_url, path, json=json, **kwargs)


async def finance_get(path: str, **kwargs: Any) -> dict[str, Any]:
    """Emare Finance'den GET isteği."""
    from config.settings import get_settings
    return await _request("GET", get_settings().emare_finance_url, path, **kwargs)


async def flow_trigger(workflow_id: str, payload: dict | None = None) -> dict[str, Any]:
    """Emare Flow'da iş akışı tetikler."""
    from config.settings import get_settings
    return await _request("POST", get_settings().emare_flow_url,
                          f"/api/workflows/{workflow_id}/trigger", json=payload or {})


async def flow_status(workflow_id: str, run_id: str) -> dict[str, Any]:
    """Emare Flow iş akışı durumunu sorgular."""
    from config.settings import get_settings
    return await _request("GET", get_settings().emare_flow_url,
                          f"/api/workflows/{workflow_id}/runs/{run_id}")


async def ai_generate(prompt: str, model: str = "llama") -> dict[str, Any]:
    """Emare AI (self-hosted LLM) üzerinden metin üretir."""
    from config.settings import get_settings
    return await _request("POST", get_settings().emare_ai_url, "/v1/generate",
                          json={"prompt": prompt, "model": model})


async def hive_assign(task: dict[str, Any]) -> dict[str, Any]:
    """Hive Coordinator'a görev atar."""
    from config.settings import get_settings
    return await _request("POST", get_settings().emare_hive_url,
                          "/api/v1/tasks", json=task)


async def oracle_query(sql: str, params: dict | None = None) -> dict[str, Any]:
    """ZeusDB / EmareOracle'a SQL sorgusu gönderir."""
    from config.settings import get_settings
    return await _request("POST", get_settings().emare_oracle_url, "/query",
                          json={"sql": sql, "params": params or {}})
