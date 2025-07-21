from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.interfaces.wallet_repository import WalletRepository
from app.entity.wallet import Wallet
from app.models.wallet import Wallet as DbWallet


class SqlAlchemyWalletRepository(WalletRepository):
    """
    Реализация репозитория кошельков с SQLAlchemy.
    """

    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self.sessionmaker = sessionmaker

    async def get_by_uuid(self, uuid: UUID) -> Wallet | None:
        """
        Получить кошелек по UUID.

        :param uuid: Идентификатор кошелька.
        :return: Wallet или None, если не найден.
        """
        async with self.sessionmaker() as session:
            db_wallet = await session.get(DbWallet, uuid)
            if db_wallet is None:
                return None
            return Wallet(uuid=db_wallet.id, balance=db_wallet.balance)

    async def save(self, wallet: Wallet) -> None:
        """
        Сохранить кошелек: обновить баланс или создать новый.

        :param wallet: Экземпляр Wallet.
        """
        async with self.sessionmaker() as session:
            db_wallet = await session.get(DbWallet, wallet.uuid)
            if db_wallet is None:
                db_wallet = DbWallet(id=wallet.uuid, balance=wallet.balance)
                session.add(db_wallet)
            else:
                db_wallet.balance = wallet.balance
            await session.commit()
