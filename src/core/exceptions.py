"""
Emare SuperApp — Özel Exception Sınıfları
"""


class SuperAppError(Exception):
    """Temel SuperApp hatası."""

    def __init__(self, message: str = "Bir hata oluştu", code: int = 500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class NotFoundError(SuperAppError):
    """Kayıt bulunamadı."""

    def __init__(self, resource: str = "Kayıt"):
        super().__init__(f"{resource} bulunamadı", 404)


class AuthenticationError(SuperAppError):
    """Kimlik doğrulama hatası."""

    def __init__(self, message: str = "Kimlik doğrulama başarısız"):
        super().__init__(message, 401)


class AuthorizationError(SuperAppError):
    """Yetkilendirme hatası."""

    def __init__(self, message: str = "Bu işlem için yetkiniz yok"):
        super().__init__(message, 403)


class ValidationError(SuperAppError):
    """Doğrulama hatası."""

    def __init__(self, message: str = "Geçersiz veri"):
        super().__init__(message, 422)


class DuplicateError(SuperAppError):
    """Tekrarlanan kayıt hatası."""

    def __init__(self, resource: str = "Kayıt"):
        super().__init__(f"{resource} zaten mevcut", 409)


class RateLimitError(SuperAppError):
    """İstek limiti aşıldı."""

    def __init__(self):
        super().__init__("Çok fazla istek — lütfen bekleyin", 429)
