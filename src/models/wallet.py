"""
Emare SuperApp — Wallet Modeli
"""
from sqlalchemy import String, Numeric, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from .base import BaseModel
import enum


class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PAYMENT = "payment"


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Wallet(BaseModel):
    """Kullanıcı cüzdanı."""

    __tablename__ = "wallets"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    balance: Mapped[float] = mapped_column(Numeric(12, 2), default=0.00)
    currency: Mapped[str] = mapped_column(String(3), default="TRY")
    is_frozen: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<Wallet user={self.user_id} balance={self.balance}>"


class Transaction(BaseModel):
    """Cüzdan işlemi."""

    __tablename__ = "transactions"

    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"))
    type: Mapped[str] = mapped_column(Enum(TransactionType))
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    reference_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    def __repr__(self):
        return f"<Transaction {self.type} {self.amount}>"
