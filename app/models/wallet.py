from sqlalchemy import Column, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.models import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        comment='Уникальный идентификатор кошелька',
    )

    balance = Column(
        Integer,
        nullable=False,
        default=0,
        server_default='0',
        comment='Текущий баланс в минимальных единицах (копейки, центы)',
    )

    __table_args__ = (
        CheckConstraint('balance >= 0', name='non_negative_balance'),
        {'comment': 'Кошельки пользователей'},
    )

    def __repr__(self):
        return f'<Wallet {self.id}, balance={self.balance}>'
