"""Email Service — asenkron e-posta gönderim servisi."""

from __future__ import annotations

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

import aiosmtplib

from src.core.config import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# E-posta Gönderimi
# ---------------------------------------------------------------------------

async def send_email(
    to: str | list[str],
    subject: str,
    body: str,
    *,
    html: bool = False,
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
) -> dict[str, Any]:
    """Asenkron e-posta gönderir.

    Args:
        to: Alıcı adresi veya adresleri.
        subject: Konu satırı.
        body: E-posta içeriği (düz metin veya HTML).
        html: İçerik HTML ise ``True``.
        cc: Carbon-copy adresleri.
        bcc: Blind carbon-copy adresleri.

    Returns:
        Gönderim sonuç bilgileri.
    """
    recipients = [to] if isinstance(to, str) else list(to)
    if cc:
        recipients.extend(cc)
    if bcc:
        recipients.extend(bcc)

    msg = MIMEMultipart("alternative")
    msg["From"] = settings.SMTP_FROM  # type: ignore[attr-defined]
    msg["To"] = ", ".join([to] if isinstance(to, str) else to)
    msg["Subject"] = subject

    if cc:
        msg["Cc"] = ", ".join(cc)

    content_type = "html" if html else "plain"
    msg.attach(MIMEText(body, content_type, "utf-8"))

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,  # type: ignore[attr-defined]
            port=settings.SMTP_PORT,  # type: ignore[attr-defined]
            username=settings.SMTP_USER,  # type: ignore[attr-defined]
            password=settings.SMTP_PASS,  # type: ignore[attr-defined]
            use_tls=settings.SMTP_TLS,  # type: ignore[attr-defined]
            recipients=recipients,
        )
        logger.info("E-posta gönderildi: konu='%s' alıcı=%s", subject, recipients)
        return {"success": True, "recipients": recipients}

    except Exception as exc:
        logger.error("E-posta gönderim hatası: %s", exc)
        return {"success": False, "error": str(exc), "recipients": recipients}


# ---------------------------------------------------------------------------
# Şablon Tabanlı Gönderim
# ---------------------------------------------------------------------------

async def send_template_email(
    to: str | list[str],
    template_name: str,
    context: dict[str, Any],
    subject: str | None = None,
) -> dict[str, Any]:
    """Şablon kullanarak e-posta gönderir.

    Args:
        to: Alıcı adresi.
        template_name: Şablon adı (ör. ``welcome``, ``password_reset``).
        context: Şablona geçirilecek değişkenler.
        subject: Konu satırı (şablondan da okunabilir).

    Returns:
        Gönderim sonuç bilgileri.
    """
    # TODO: Şablon dosyasını oku ve context ile render et (Jinja2 vb.)
    templates: dict[str, dict[str, str]] = {
        "welcome": {
            "subject": "Emare SuperApp'e Hoş Geldiniz!",
            "body": "<h1>Merhaba {full_name}!</h1><p>Emare ailesine katıldığınız için teşekkürler.</p>",
        },
        "password_reset": {
            "subject": "Şifre Sıfırlama Talebi",
            "body": "<p>Şifrenizi sıfırlamak için bağlantıya tıklayın: {reset_url}</p>",
        },
        "notification": {
            "subject": "Yeni Bildirim",
            "body": "<p>{message}</p>",
        },
    }

    template = templates.get(template_name)
    if not template:
        return {"success": False, "error": f"Şablon bulunamadı: {template_name}"}

    rendered_subject = subject or template["subject"]
    rendered_body = template["body"].format_map(context)

    return await send_email(to, rendered_subject, rendered_body, html=True)
