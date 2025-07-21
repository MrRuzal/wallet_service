from abc import ABC, abstractmethod
from app.entity.wallet import Wallet
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession


class WalletRepository(ABC):
    @abstractmethod
    async def get_by_uuid(
        self, session: AsyncSession, uuid: UUID
    ) -> Wallet | None:
        """
        Получить кошелек по UUID с блокировкой (FOR UPDATE).

        :param session: AsyncSession для выполнения запроса.
        :param uuid: Идентификатор кошелька.
        :return: Wallet или None, если не найден.
        """
        pass

    @abstractmethod
    async def save(self, session: AsyncSession, wallet: Wallet) -> None:
        """
        Сохранить кошелек: обновить баланс или создать новый.

        :param session: AsyncSession для выполнения запроса.
        :param wallet: Экземпляр Wallet.
        """
        pass
