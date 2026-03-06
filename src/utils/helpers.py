"""Helpers — genel yardımcı fonksiyonlar."""

from __future__ import annotations

import re
import unicodedata
from decimal import Decimal
from uuid import uuid4


# ---------------------------------------------------------------------------
# Slug Üretimi
# ---------------------------------------------------------------------------

def slugify(text: str, max_length: int = 120) -> str:
    """Metni URL-dostu slug formatına dönüştürür.

    Türkçe karakterleri ASCII'ye çevirir, özel karakterleri kaldırır.

    Args:
        text: Dönüştürülecek metin.
        max_length: Maksimum slug uzunluğu.

    Returns:
        Küçük harfli, tire-ayrılmış slug.

    >>> slugify("Emare Süper Uygulama!")
    'emare-super-uygulama'
    """
    # Türkçe karakter haritası
    tr_map = str.maketrans({
        "ç": "c", "Ç": "C",
        "ğ": "g", "Ğ": "G",
        "ı": "i", "İ": "I",
        "ö": "o", "Ö": "O",
        "ş": "s", "Ş": "S",
        "ü": "u", "Ü": "U",
    })
    text = text.translate(tr_map)

    # Unicode normalize + ASCII'ye çevir
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()

    # Alfanümerik olmayan karakterleri tire yap
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")

    return text[:max_length]


# ---------------------------------------------------------------------------
# Benzersiz Kimlik Üretimi
# ---------------------------------------------------------------------------

def generate_id(prefix: str = "") -> str:
    """Opsiyonel ön-ekli benzersiz kimlik üretir.

    Args:
        prefix: Kimlik öneki (ör. ``usr``, ``txn``).

    Returns:
        UUID4 tabanlı kimlik.

    >>> len(generate_id("usr")) > 4
    True
    """
    uid = uuid4().hex
    return f"{prefix}_{uid}" if prefix else uid


# ---------------------------------------------------------------------------
# Para Biçimlendirme
# ---------------------------------------------------------------------------

def format_currency(
    amount: Decimal | float | int | str,
    currency: str = "TRY",
    locale: str = "tr",
) -> str:
    """Tutarı para birimi ile biçimlendirir.

    Args:
        amount: Tutar değeri.
        currency: Para birimi kodu.
        locale: Biçimlendirme yerel ayarı.

    Returns:
        Biçimlendirilmiş tutar dizesi.

    >>> format_currency(1234.5)
    '1.234,50 TRY'
    >>> format_currency(1234.5, "USD", "en")
    '1,234.50 USD'
    """
    value = Decimal(str(amount))
    abs_value = abs(value)

    # Tam kısım ve ondalık ayır
    integer_part = int(abs_value)
    decimal_part = abs_value - integer_part
    decimal_str = f"{decimal_part:.2f}"[2:]  # ".XX" -> "XX"

    # Binlik ayraçlı tam kısım
    int_str = f"{integer_part:,}"

    if locale == "tr":
        # Türkçe: binlik nokta, ondalık virgül
        int_str = int_str.replace(",", ".")
        formatted = f"{int_str},{decimal_str}"
    else:
        # Varsayılan (en): binlik virgül, ondalık nokta
        formatted = f"{int_str}.{decimal_str}"

    sign = "-" if value < 0 else ""
    return f"{sign}{formatted} {currency}"


# ---------------------------------------------------------------------------
# Metin Kısaltma
# ---------------------------------------------------------------------------

def truncate(text: str, max_length: int = 100, suffix: str = "…") -> str:
    """Uzun metni belirtilen uzunlukta kırpar.

    Args:
        text: Kırpılacak metin.
        max_length: Maksimum karakter sayısı (sonek dahil).
        suffix: Kırpma soneki.

    Returns:
        Kırpılmış metin.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
