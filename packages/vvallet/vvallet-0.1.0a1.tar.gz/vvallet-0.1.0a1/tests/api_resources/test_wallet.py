# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from vvallet import Vvallet, AsyncVvallet
from tests.utils import assert_matches_type
from vvallet.types import (
    WalletCreateResponse,
    WalletListBalancesResponse,
    WalletCreateAddressResponse,
    WalletListAddressesResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWallet:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Vvallet) -> None:
        wallet = client.wallet.create(
            master_password="password123",
            network="base-sepolia",
        )
        assert_matches_type(WalletCreateResponse, wallet, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Vvallet) -> None:
        response = client.wallet.with_raw_response.create(
            master_password="password123",
            network="base-sepolia",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        wallet = response.parse()
        assert_matches_type(WalletCreateResponse, wallet, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Vvallet) -> None:
        with client.wallet.with_streaming_response.create(
            master_password="password123",
            network="base-sepolia",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            wallet = response.parse()
            assert_matches_type(WalletCreateResponse, wallet, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_address(self, client: Vvallet) -> None:
        wallet = client.wallet.create_address(
            master_password="password123",
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        )
        assert_matches_type(WalletCreateAddressResponse, wallet, path=["response"])

    @parametrize
    def test_raw_response_create_address(self, client: Vvallet) -> None:
        response = client.wallet.with_raw_response.create_address(
            master_password="password123",
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        wallet = response.parse()
        assert_matches_type(WalletCreateAddressResponse, wallet, path=["response"])

    @parametrize
    def test_streaming_response_create_address(self, client: Vvallet) -> None:
        with client.wallet.with_streaming_response.create_address(
            master_password="password123",
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            wallet = response.parse()
            assert_matches_type(WalletCreateAddressResponse, wallet, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_addresses(self, client: Vvallet) -> None:
        wallet = client.wallet.list_addresses(
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        )
        assert_matches_type(WalletListAddressesResponse, wallet, path=["response"])

    @parametrize
    def test_raw_response_list_addresses(self, client: Vvallet) -> None:
        response = client.wallet.with_raw_response.list_addresses(
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        wallet = response.parse()
        assert_matches_type(WalletListAddressesResponse, wallet, path=["response"])

    @parametrize
    def test_streaming_response_list_addresses(self, client: Vvallet) -> None:
        with client.wallet.with_streaming_response.list_addresses(
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            wallet = response.parse()
            assert_matches_type(WalletListAddressesResponse, wallet, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_balances(self, client: Vvallet) -> None:
        wallet = client.wallet.list_balances(
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        )
        assert_matches_type(WalletListBalancesResponse, wallet, path=["response"])

    @parametrize
    def test_raw_response_list_balances(self, client: Vvallet) -> None:
        response = client.wallet.with_raw_response.list_balances(
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        wallet = response.parse()
        assert_matches_type(WalletListBalancesResponse, wallet, path=["response"])

    @parametrize
    def test_streaming_response_list_balances(self, client: Vvallet) -> None:
        with client.wallet.with_streaming_response.list_balances(
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            wallet = response.parse()
            assert_matches_type(WalletListBalancesResponse, wallet, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncWallet:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncVvallet) -> None:
        wallet = await async_client.wallet.create(
            master_password="password123",
            network="base-sepolia",
        )
        assert_matches_type(WalletCreateResponse, wallet, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncVvallet) -> None:
        response = await async_client.wallet.with_raw_response.create(
            master_password="password123",
            network="base-sepolia",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        wallet = await response.parse()
        assert_matches_type(WalletCreateResponse, wallet, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncVvallet) -> None:
        async with async_client.wallet.with_streaming_response.create(
            master_password="password123",
            network="base-sepolia",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            wallet = await response.parse()
            assert_matches_type(WalletCreateResponse, wallet, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_address(self, async_client: AsyncVvallet) -> None:
        wallet = await async_client.wallet.create_address(
            master_password="password123",
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        )
        assert_matches_type(WalletCreateAddressResponse, wallet, path=["response"])

    @parametrize
    async def test_raw_response_create_address(self, async_client: AsyncVvallet) -> None:
        response = await async_client.wallet.with_raw_response.create_address(
            master_password="password123",
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        wallet = await response.parse()
        assert_matches_type(WalletCreateAddressResponse, wallet, path=["response"])

    @parametrize
    async def test_streaming_response_create_address(self, async_client: AsyncVvallet) -> None:
        async with async_client.wallet.with_streaming_response.create_address(
            master_password="password123",
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            wallet = await response.parse()
            assert_matches_type(WalletCreateAddressResponse, wallet, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_addresses(self, async_client: AsyncVvallet) -> None:
        wallet = await async_client.wallet.list_addresses(
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        )
        assert_matches_type(WalletListAddressesResponse, wallet, path=["response"])

    @parametrize
    async def test_raw_response_list_addresses(self, async_client: AsyncVvallet) -> None:
        response = await async_client.wallet.with_raw_response.list_addresses(
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        wallet = await response.parse()
        assert_matches_type(WalletListAddressesResponse, wallet, path=["response"])

    @parametrize
    async def test_streaming_response_list_addresses(self, async_client: AsyncVvallet) -> None:
        async with async_client.wallet.with_streaming_response.list_addresses(
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            wallet = await response.parse()
            assert_matches_type(WalletListAddressesResponse, wallet, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_balances(self, async_client: AsyncVvallet) -> None:
        wallet = await async_client.wallet.list_balances(
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        )
        assert_matches_type(WalletListBalancesResponse, wallet, path=["response"])

    @parametrize
    async def test_raw_response_list_balances(self, async_client: AsyncVvallet) -> None:
        response = await async_client.wallet.with_raw_response.list_balances(
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        wallet = await response.parse()
        assert_matches_type(WalletListBalancesResponse, wallet, path=["response"])

    @parametrize
    async def test_streaming_response_list_balances(self, async_client: AsyncVvallet) -> None:
        async with async_client.wallet.with_streaming_response.list_balances(
            wallet_id="c3e0c6b3-ea34-46fd-97fc-dca4fe4b3009",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            wallet = await response.parse()
            assert_matches_type(WalletListBalancesResponse, wallet, path=["response"])

        assert cast(Any, response.is_closed) is True
