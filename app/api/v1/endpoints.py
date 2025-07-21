from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.schemas import WalletOperation, WalletBalance
from app.usecases.wallet_service import WalletService
from uuid import UUID
from app.infrastructure.wallet_repository import SqlAlchemyWalletRepository
from app.infrastructure.database import async_session

router = APIRouter()

repository = SqlAlchemyWalletRepository()
service = WalletService(repository, async_session)


@router.post("/wallets/{wallet_id}/operation", response_model=WalletBalance)
async def operate_wallet(wallet_id: UUID, operation: WalletOperation):
    try:
        updated_wallet = await service.process_operation(wallet_id, operation)
        return WalletBalance(
            uuid=str(updated_wallet.uuid), balance=updated_wallet.balance
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/wallets/{wallet_id}", response_model=WalletBalance)
async def get_wallet_balance(wallet_id: UUID):
    wallet = await service.get_balance(wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return WalletBalance(uuid=str(wallet.uuid), balance=wallet.balance)
