from uuid import UUID
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.api.v1.schemas import OperationType, WalletOperation
from app.interfaces.wallet_repository import WalletRepository
from app.entity.wallet import Wallet
from app.common.logs import logger


class WalletService:
    """
    Сервис для обработки операций с кошельками.
    """

    def __init__(
        self,
        repository: WalletRepository,
        sessionmaker: async_sessionmaker[AsyncSession],
    ):
        self.repository = repository
        self.sessionmaker = sessionmaker

    async def get_wallet(
        self, uuid: UUID, session: AsyncSession
    ) -> Wallet | None:
        """
        Получить кошелёк по UUID с блокировкой (for update).

        :param uuid: UUID кошелька.
        :param session: сессия для работы с БД.
        :return: Экземпляр Wallet или None.
        :note: При чтении кошелёк блокируется для предотвращения гонок данных.
        """
        return await self.repository.get_by_uuid(session, uuid)

    async def get_balance(self, uuid: UUID) -> Wallet:
        """
        Получить кошелёк по UUID (с балансом).

        :param uuid: UUID кошелька.
        :return: Экземпляр Wallet с балансом.
        :raises ValueError: Если кошелёк не найден.
        """
        async with self.sessionmaker() as session:
            wallet = await self.get_wallet(uuid, session)
            if wallet is None:
                logger.error(f"Wallet {uuid} not found when getting balance")
                raise ValueError("Wallet not found")
            return wallet

    async def process_operation(
        self, uuid: UUID, operation: WalletOperation
    ) -> Wallet:
        """
        Обработать операцию с кошельком (пополнение или снятие).

        :param uuid: UUID кошелька.
        :param operation: Объект операции с типом и суммой.
        :return: Обновленный экземпляр Wallet.
        :raises ValueError: При ошибках валидации или выполнении операции.
        """
        async with self.sessionmaker() as session:
            async with session.begin():
                try:
                    if operation.amount <= 0:
                        raise ValueError("Amount must be positive")

                    wallet = await self.get_wallet(uuid, session)
                    if wallet is None:
                        wallet = Wallet(uuid=uuid, balance=0)

                    if operation.operation_type == OperationType.DEPOSIT:
                        wallet.deposit(operation.amount)
                    elif operation.operation_type == OperationType.WITHDRAW:
                        wallet.withdraw(operation.amount)
                    else:
                        raise ValueError(
                            f"Unsupported operation type: {operation.operation_type}"
                        )

                    await self.repository.save(wallet, session)
                    logger.info(
                        f"Processed {operation.operation_type} of {operation.amount} for wallet {uuid}"
                    )
                    return wallet

                except ValueError as e:
                    logger.error(
                        f"Error processing operation for wallet {uuid}: {e}"
                    )
                    raise
