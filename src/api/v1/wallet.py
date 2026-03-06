"""
Emare SuperApp — Wallet API Endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class WalletResponse(BaseModel):
    id: int
    user_id: int
    balance: float
    currency: str = "TRY"


class TransferRequest(BaseModel):
    to_user_id: int
    amount: float
    description: Optional[str] = None


class TransactionResponse(BaseModel):
    id: int
    type: str
    amount: float
    status: str
    description: Optional[str] = None


@router.get("/balance", response_model=WalletResponse)
async def get_balance():
    """Cüzdan bakiyesi."""
    return WalletResponse(id=1, user_id=1, balance=0.00)


@router.post("/deposit")
async def deposit(amount: float):
    """Para yatır."""
    return {"message": f"{amount} TRY yatırıldı", "new_balance": amount}


@router.post("/withdraw")
async def withdraw(amount: float):
    """Para çek."""
    return {"message": f"{amount} TRY çekildi"}


@router.post("/transfer")
async def transfer(data: TransferRequest):
    """Para transferi."""
    return {"message": f"{data.amount} TRY kullanıcı {data.to_user_id}'ye gönderildi"}


@router.get("/transactions", response_model=List[TransactionResponse])
async def list_transactions():
    """İşlem geçmişi."""
    return []
