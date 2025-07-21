from dataclasses import dataclass


@dataclass
class Wallet:
    """Кошелек с балансом."""

    uuid: str
    balance: int = 0

    def deposit(self, amount: int):
        """
        Пополнить кошелек.

        :param amount: Сумма пополнения, должна быть положительной.
        :raises ValueError: Если сумма не положительная.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: int):
        """
        Снять средства с кошелька.

        :param amount: Сумма снятия, должна быть положительной.
        :raises ValueError: Если сумма не положительная или превышает баланс.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
