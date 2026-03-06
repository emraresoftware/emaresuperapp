"""AI Assistant Service — Gemini / OpenAI entegrasyonlu yapay zeka asistanı."""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from src.core.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Ortak HTTP istemcisi
# ---------------------------------------------------------------------------

_http_timeout = httpx.Timeout(timeout=60.0)


# ---------------------------------------------------------------------------
# OpenAI Chat Completion
# ---------------------------------------------------------------------------

async def ask_openai(
    prompt: str,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    system_message: str | None = None,
) -> dict[str, Any]:
    """OpenAI Chat Completion API üzerinden yanıt alır.

    Args:
        prompt: Kullanıcı mesajı.
        model: Kullanılacak model adı.
        temperature: Yaratıcılık parametresi (0-2).
        max_tokens: Maksimum yanıt uzunluğu.
        system_message: Opsiyonel sistem mesajı.

    Returns:
        API yanıtını içeren sözlük.
    """
    api_key = settings.OPENAI_API_KEY  # type: ignore[attr-defined]
    if not api_key:
        raise ValueError("OPENAI_API_KEY ayarlanmamış.")

    messages: list[dict[str, str]] = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    async with httpx.AsyncClient(timeout=_http_timeout) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        )
        response.raise_for_status()
        data = response.json()

    return {
        "model": model,
        "content": data["choices"][0]["message"]["content"],
        "usage": data.get("usage"),
    }


# ---------------------------------------------------------------------------
# Google Gemini
# ---------------------------------------------------------------------------

async def ask_gemini(
    prompt: str,
    model: str = "gemini-pro",
    temperature: float = 0.7,
    max_output_tokens: int = 2048,
) -> dict[str, Any]:
    """Google Gemini API üzerinden yanıt alır.

    Args:
        prompt: Kullanıcı mesajı.
        model: Kullanılacak model adı.
        temperature: Yaratıcılık parametresi.
        max_output_tokens: Maksimum yanıt uzunluğu.

    Returns:
        API yanıtını içeren sözlük.
    """
    api_key = settings.GEMINI_API_KEY  # type: ignore[attr-defined]
    if not api_key:
        raise ValueError("GEMINI_API_KEY ayarlanmamış.")

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
        },
    }

    async with httpx.AsyncClient(timeout=_http_timeout) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return {
        "model": model,
        "content": text,
        "usage": data.get("usageMetadata"),
    }


# ---------------------------------------------------------------------------
# Genel Arayüz — sağlayıcı seçimi
# ---------------------------------------------------------------------------

async def ask(
    prompt: str,
    provider: str = "openai",
    **kwargs: Any,
) -> dict[str, Any]:
    """Yapılandırma veya tercih bazlı AI sağlayıcısını seçerek yanıt alır.

    Args:
        prompt: Kullanıcı mesajı.
        provider: ``"openai"`` veya ``"gemini"``.
        **kwargs: Sağlayıcıya özel ek parametreler.

    Returns:
        AI yanıtını içeren sözlük.
    """
    providers = {
        "openai": ask_openai,
        "gemini": ask_gemini,
    }

    handler = providers.get(provider)
    if handler is None:
        raise ValueError(f"Desteklenmeyen AI sağlayıcı: {provider}")

    logger.info("AI isteği — sağlayıcı=%s prompt_uzunluk=%d", provider, len(prompt))
    return await handler(prompt, **kwargs)


# ---------------------------------------------------------------------------
# Sohbet Geçmişi (basit bellek-içi)
# ---------------------------------------------------------------------------

_conversations: dict[str, list[dict[str, str]]] = {}


async def chat(
    session_id: str,
    user_message: str,
    provider: str = "openai",
) -> dict[str, Any]:
    """Oturum bazlı sohbet — geçmiş mesajları bağlam olarak gönderir.

    Args:
        session_id: Sohbet oturumu kimliği.
        user_message: Kullanıcının yeni mesajı.
        provider: AI sağlayıcı.

    Returns:
        Asistan yanıtını içeren sözlük.
    """
    history = _conversations.setdefault(session_id, [])
    history.append({"role": "user", "content": user_message})

    # Geçmişi tek bir prompt olarak birleştir
    full_prompt = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in history
    )

    result = await ask(full_prompt, provider=provider)
    assistant_msg = result["content"]

    history.append({"role": "assistant", "content": assistant_msg})

    return {
        "session_id": session_id,
        "response": assistant_msg,
        "history_length": len(history),
    }
