from abc import ABC, abstractmethod
from typing import Optional
from app.entity.wallet import Wallet


class WalletRepository(ABC):
    @abstractmethod
    async def get_by_uuid(self, uuid: str) -> Optional[Wallet]:
        """Получить кошелек по UUID"""
        pass

    @abstractmethod
    async def save(self, wallet: Wallet) -> None:
        """Сохранить изменения кошелька"""
        pass
