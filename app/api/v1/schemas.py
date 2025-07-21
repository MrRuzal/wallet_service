from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletOperation(BaseModel):
    """
    Запрос для выполнения операции с кошельком.

    :param operation_type (OperationType): Тип операции (пополнение или снятие).
    :param amount (int): Положительное число, сумма операции в минимальных единицах.
    """

    operation_type: OperationType
    amount: int = Field(..., gt=0, description="Положительная сумма операции")


class WalletBalance(BaseModel):
    """
    Текущий баланс кошелька.

    param: uuid (UUID): Уникальный идентификатор кошелька.
    param: balance (int): Баланс в минимальных единицах.
    """

    uuid: UUID
    balance: int
