import pytest
from uuid import UUID, uuid4
from httpx import AsyncClient
from fastapi import FastAPI
from app.api.v1 import endpoints
from app.usecases.wallet_service import WalletService
from app.entity.wallet import Wallet
from app.api.v1.schemas import WalletOperation, WalletBalance


class TestWalletService:
    """Тестовый сервис кошельков для тестирования без БД."""

    def __init__(self):
        self.wallets: dict[UUID, Wallet] = {}

    async def get_balance(self, wallet_id: UUID) -> Wallet | None:
        """
        Получить баланс кошелька по UUID.

        :param wallet_id: UUID кошелька
        :return: Wallet или None, если кошелек не найден
        """
        return self.wallets.get(wallet_id)

    async def process_operation(
        self, wallet_id: UUID, operation: WalletOperation
    ) -> Wallet:
        """
        Обработать операцию с кошельком.

        :param wallet_id: UUID кошелька
        :param operation: операция (депозит или вывод)
        :return: обновленный Wallet
        :raises ValueError: если операция неизвестна или баланс недостаточен
        """
        wallet = self.wallets.get(wallet_id)
        if wallet is None:
            wallet = Wallet(uuid=str(wallet_id), balance=0)

        if operation.operation_type == "DEPOSIT":
            wallet.balance += operation.amount
        elif operation.operation_type == "WITHDRAW":
            if operation.amount > wallet.balance:
                raise ValueError("Insufficient balance")
            wallet.balance -= operation.amount
        else:
            raise ValueError("Unknown operation type")

        self.wallets[wallet_id] = wallet
        return wallet


@pytest.fixture
def app() -> FastAPI:
    """
    Фикстура FastAPI приложения с мок-сервисом кошельков.
    """
    test_app = FastAPI()
    test_app.include_router(endpoints.router, prefix="/api/v1")

    mock_wallet_service = TestWalletService()

    async def override_get_wallet_service() -> WalletService:
        return mock_wallet_service

    test_app.dependency_overrides[endpoints.get_wallet_service] = (
        override_get_wallet_service
    )
    return test_app


@pytest.mark.asyncio
async def test_get_wallet_balance_not_found(app: FastAPI):
    """
    Тест запроса баланса несуществующего кошелька.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        wallet_id = uuid4()
        response = await client.get(f"/api/v1/wallets/{wallet_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Wallet not found"}


@pytest.mark.asyncio
async def test_post_wallet_deposit_and_get_balance(app: FastAPI):
    """
    Тест депозита и получения баланса кошелька.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        wallet_id = uuid4()
        deposit_data = {"operation_type": "DEPOSIT", "amount": 1000}

        response = await client.post(
            f"/api/v1/wallets/{wallet_id}/operation", json=deposit_data
        )
        assert response.status_code == 200
        body = response.json()
        assert body["uuid"] == str(wallet_id)
        assert body["balance"] == 1000

        response = await client.get(f"/api/v1/wallets/{wallet_id}")
        assert response.status_code == 200
        body = response.json()
        assert body["uuid"] == str(wallet_id)
        assert body["balance"] == 1000


@pytest.mark.asyncio
async def test_post_wallet_withdraw_insufficient_balance(app: FastAPI):
    """
    Тест вывода средств при недостаточном балансе (ожидается ошибка).
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        wallet_id = uuid4()

        deposit_data = {"operation_type": "DEPOSIT", "amount": 500}
        await client.post(
            f"/api/v1/wallets/{wallet_id}/operation", json=deposit_data
        )

        withdraw_data = {"operation_type": "WITHDRAW", "amount": 1000}
        response = await client.post(
            f"/api/v1/wallets/{wallet_id}/operation", json=withdraw_data
        )
        assert response.status_code == 400
        assert "Insufficient balance" in response.text
