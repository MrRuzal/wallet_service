from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.schemas import WalletOperation, WalletBalance
from app.usecases.wallet_service import WalletService
from uuid import UUID
from app.infrastructure.wallet_repository import SqlAlchemyWalletRepository
from app.infrastructure.database import async_session

from app.common.logs import logger

router = APIRouter()


def get_wallet_service() -> WalletService:
    repository = SqlAlchemyWalletRepository(async_session)
    return WalletService(repository)


@router.post("/wallets/{wallet_id}/operation", response_model=WalletBalance)
async def operate_wallet(
    wallet_id: UUID,
    operation: WalletOperation,
    service: WalletService = Depends(get_wallet_service),
):
    logger.info(
        "Processing operation: type='%s', wallet_id='%s', amount=%s",
        operation.operation_type,
        wallet_id,
        operation.amount,
    )
    try:
        updated_wallet = await service.process_operation(wallet_id, operation)
        return WalletBalance(
            uuid=str(updated_wallet.uuid), balance=updated_wallet.balance
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/wallets/{wallet_id}", response_model=WalletBalance)
async def get_wallet_balance(
    wallet_id: UUID,
    service: WalletService = Depends(get_wallet_service),
):
    logger.info("Fetching balance for wallet_id='%s'", wallet_id)
    wallet = await service.get_balance(wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return WalletBalance(uuid=str(wallet.uuid), balance=wallet.balance)
