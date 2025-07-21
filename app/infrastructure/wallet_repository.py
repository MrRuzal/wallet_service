from sqlalchemy import select
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.interfaces.wallet_repository import WalletRepository
from app.entity.wallet import Wallet
from app.models.wallet import Wallet as DbWallet


class SqlAlchemyWalletRepository(WalletRepository):
    """
    Реализация репозитория кошельков с SQLAlchemy.
    """

    async def get_by_uuid(
        self, session: AsyncSession, uuid: UUID
    ) -> Wallet | None:
        """
        Получить кошелек по UUID с блокировкой (FOR UPDATE).

        :param session: AsyncSession для выполнения запроса.
        :param uuid: Идентификатор кошелька.
        :return: Wallet или None, если не найден.
        """
        result = await session.execute(
            select(DbWallet).where(DbWallet.id == uuid).with_for_update()
        )
        db_wallet = result.scalar_one_or_none()
        if db_wallet is None:
            return None
        return Wallet(uuid=db_wallet.id, balance=db_wallet.balance)

    async def save(self, session: AsyncSession, wallet: Wallet) -> None:
        """
        Сохранить кошелек: обновить баланс или создать новый.

        :param session: AsyncSession для выполнения запроса.
        :param wallet: Экземпляр Wallet.
        """
        db_wallet = await session.get(DbWallet, wallet.uuid)
        if db_wallet is None:
            db_wallet = DbWallet(id=wallet.uuid, balance=wallet.balance)
            session.add(db_wallet)
        else:
            db_wallet.balance = wallet.balance
        await session.commit()
