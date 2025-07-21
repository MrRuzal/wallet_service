import pytest
from uuid import UUID, uuid4
from httpx import AsyncClient
from fastapi import FastAPI
from unittest.mock import AsyncMock, patch

from app.api.v1 import endpoints
from app.api.v1.schemas import WalletOperation, WalletBalance


@pytest.fixture
def app() -> FastAPI:
    test_app = FastAPI()
    test_app.include_router(endpoints.router, prefix="/api/v1")
    return test_app


@pytest.mark.asyncio
async def test_get_wallet_balance_not_found(app: FastAPI):
    wallet_id = uuid4()

    with patch.object(
        endpoints.service, "get_balance", new=AsyncMock(return_value=None)
    ):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(f"/api/v1/wallets/{wallet_id}")
            assert response.status_code == 404
            assert response.json() == {"detail": "Wallet not found"}


@pytest.mark.asyncio
async def test_post_wallet_deposit_and_get_balance(app: FastAPI):
    wallet_id = uuid4()
    wallet_data = WalletBalance(uuid=wallet_id, balance=1000)

    with patch.object(
        endpoints.service,
        "process_operation",
        new=AsyncMock(return_value=wallet_data),
    ):
        with patch.object(
            endpoints.service,
            "get_balance",
            new=AsyncMock(return_value=wallet_data),
        ):
            async with AsyncClient(app=app, base_url="http://test") as client:
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
    wallet_id = uuid4()

    async def mock_process_operation(wallet_id, operation):
        raise ValueError("Insufficient balance")

    with patch.object(
        endpoints.service, "process_operation", new=mock_process_operation
    ):
        async with AsyncClient(app=app, base_url="http://test") as client:
            deposit_data = {"operation_type": "WITHDRAW", "amount": 1000}

            response = await client.post(
                f"/api/v1/wallets/{wallet_id}/operation", json=deposit_data
            )
            assert response.status_code == 400
            assert "Insufficient balance" in response.text
