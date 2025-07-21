from uuid import UUID
import uuid

from app.api.v1.schemas import OperationType, WalletOperation
from app.interfaces.wallet_repository import WalletRepository
from app.entity.wallet import Wallet
from app.common.logs import logger


class WalletService:
    """
    Сервис для обработки операций с кошельками.
    """

    def __init__(self, repository: WalletRepository):
        self.repository = repository

    async def get_wallet(self, uuid: UUID) -> Wallet | None:
        """
        Получить кошелёк по UUID.

        :param uuid: UUID кошелька.
        :return: Экземпляр Wallet или None.
        """
        return await self.repository.get_by_uuid(uuid)

    async def operate(
        self, uuid: UUID, operation_type: OperationType, amount: int
    ) -> Wallet:
        """
        Применить операцию к кошельку: пополнение или снятие.

        :param uuid: UUID кошелька.
        :param operation_type: Тип операции.
        :param amount: Сумма операции.
        :return: Обновлённый кошелёк.
        :raises ValueError: При некорректной операции.
        """
        wallet = await self.repository.get_by_uuid(uuid)
        if wallet is None:
            wallet = Wallet(uuid=uuid, balance=0)

        if operation_type == OperationType.DEPOSIT:
            wallet.deposit(amount)
        elif operation_type == OperationType.WITHDRAW:
            wallet.withdraw(amount)
        else:
            raise ValueError(f"Unsupported operation type: {operation_type}")

        await self.repository.save(wallet)
        return wallet

    async def get_balance(self, uuid: UUID) -> Wallet:
        """
        Получить баланс кошелька.

        :param uuid: UUID кошелька.
        :return: Экземпляр Wallet.
        :raises ValueError: Если кошелёк не найден.
        """
        wallet = await self.get_wallet(uuid)
        if wallet is None:
            raise ValueError("Wallet not found")
        return wallet

    async def process_operation(
        self, uuid: UUID, operation: WalletOperation
    ) -> Wallet:
        """
        Обработать операцию с кошельком.

        :param uuid: UUID кошелька.
        :param operation: Объект операции (тип и сумма).
        :return: Обновлённый кошелёк.
        :raises ValueError: При некорректной операции или ошибке.
        """
        try:
            return await self.operate(
                uuid, operation.operation_type, operation.amount
            )
        except ValueError as e:
            logger.error(f"Error processing operation for wallet {uuid}: {e}")
            raise ValueError("Error processing operation")
