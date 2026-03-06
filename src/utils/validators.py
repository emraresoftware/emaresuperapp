"""Validators — doğrulama yardımcıları."""

from __future__ import annotations

import re


# ---------------------------------------------------------------------------
# E-posta Doğrulama
# ---------------------------------------------------------------------------

# RFC 5322 basitleştirilmiş regex
_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$"
)


def is_valid_email(email: str) -> bool:
    """E-posta adresinin geçerli biçimde olup olmadığını kontrol eder.

    Args:
        email: Doğrulanacak e-posta adresi.

    Returns:
        Geçerliyse ``True``.

    >>> is_valid_email("kullanici@emare.com")
    True
    >>> is_valid_email("gecersiz@@adres")
    False
    """
    if not email or len(email) > 320:
        return False
    return _EMAIL_REGEX.match(email) is not None


# ---------------------------------------------------------------------------
# Güçlü Şifre Doğrulama
# ---------------------------------------------------------------------------

def is_strong_password(
    password: str,
    min_length: int = 8,
    require_upper: bool = True,
    require_lower: bool = True,
    require_digit: bool = True,
    require_special: bool = True,
) -> tuple[bool, list[str]]:
    """Şifrenin güçlülük kriterlerini karşılayıp karşılamadığını kontrol eder.

    Args:
        password: Doğrulanacak şifre.
        min_length: Minimum karakter sayısı.
        require_upper: Büyük harf zorunluluğu.
        require_lower: Küçük harf zorunluluğu.
        require_digit: Rakam zorunluluğu.
        require_special: Özel karakter zorunluluğu.

    Returns:
        ``(geçerli_mi, hata_listesi)`` çifti.

    >>> is_strong_password("Emare2024!")
    (True, [])
    >>> is_strong_password("zayıf")
    (False, [...])
    """
    errors: list[str] = []

    if len(password) < min_length:
        errors.append(f"Şifre en az {min_length} karakter olmalıdır.")

    if require_upper and not re.search(r"[A-Z]", password):
        errors.append("En az bir büyük harf içermelidir.")

    if require_lower and not re.search(r"[a-z]", password):
        errors.append("En az bir küçük harf içermelidir.")

    if require_digit and not re.search(r"\d", password):
        errors.append("En az bir rakam içermelidir.")

    if require_special and not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]", password):
        errors.append("En az bir özel karakter içermelidir.")

    return (len(errors) == 0, errors)


# ---------------------------------------------------------------------------
# Telefon Numarası Doğrulama
# ---------------------------------------------------------------------------

_PHONE_REGEX = re.compile(r"^\+?[1-9]\d{7,14}$")


def is_valid_phone(phone: str) -> bool:
    """Telefon numarasının uluslararası formatta geçerli olup olmadığını kontrol eder.

    Args:
        phone: Doğrulanacak telefon numarası.

    Returns:
        Geçerliyse ``True``.

    >>> is_valid_phone("+905551234567")
    True
    >>> is_valid_phone("123")
    False
    """
    cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    return _PHONE_REGEX.match(cleaned) is not None


# ---------------------------------------------------------------------------
# TC Kimlik No Doğrulama
# ---------------------------------------------------------------------------

def is_valid_tckn(tckn: str) -> bool:
    """11 haneli TC Kimlik Numarasının algoritmik doğruluğunu kontrol eder.

    Args:
        tckn: Doğrulanacak TC Kimlik Numarası.

    Returns:
        Geçerliyse ``True``.
    """
    if not tckn or len(tckn) != 11 or not tckn.isdigit():
        return False

    digits = [int(d) for d in tckn]

    if digits[0] == 0:
        return False

    # 10. hane kontrolü
    odd_sum = sum(digits[i] for i in range(0, 9, 2))
    even_sum = sum(digits[i] for i in range(1, 8, 2))
    check_10 = (odd_sum * 7 - even_sum) % 10
    if check_10 != digits[9]:
        return False

    # 11. hane kontrolü
    total = sum(digits[:10])
    if total % 10 != digits[10]:
        return False

    return True
