# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from vvallet import Vvallet, AsyncVvallet
from tests.utils import assert_matches_type
from vvallet.types import TransferCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTransfer:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Vvallet) -> None:
        transfer = client.transfer.create(
            amount=1,
            from_={
                "address": "0xF1C7ee435E5e46C3CCef62c1eE21f97dEfe9816A",
                "wallet_id": "4a65b127-0a2e-4c5b-9a4a-85680f60eab8",
            },
            master_password="password123",
            network="base-sepolia",
            to={"address": "0x2FD2ed754fCD8748b89D5577241E76432306D5a5"},
        )
        assert_matches_type(TransferCreateResponse, transfer, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Vvallet) -> None:
        response = client.transfer.with_raw_response.create(
            amount=1,
            from_={
                "address": "0xF1C7ee435E5e46C3CCef62c1eE21f97dEfe9816A",
                "wallet_id": "4a65b127-0a2e-4c5b-9a4a-85680f60eab8",
            },
            master_password="password123",
            network="base-sepolia",
            to={"address": "0x2FD2ed754fCD8748b89D5577241E76432306D5a5"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transfer = response.parse()
        assert_matches_type(TransferCreateResponse, transfer, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Vvallet) -> None:
        with client.transfer.with_streaming_response.create(
            amount=1,
            from_={
                "address": "0xF1C7ee435E5e46C3CCef62c1eE21f97dEfe9816A",
                "wallet_id": "4a65b127-0a2e-4c5b-9a4a-85680f60eab8",
            },
            master_password="password123",
            network="base-sepolia",
            to={"address": "0x2FD2ed754fCD8748b89D5577241E76432306D5a5"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transfer = response.parse()
            assert_matches_type(TransferCreateResponse, transfer, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTransfer:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncVvallet) -> None:
        transfer = await async_client.transfer.create(
            amount=1,
            from_={
                "address": "0xF1C7ee435E5e46C3CCef62c1eE21f97dEfe9816A",
                "wallet_id": "4a65b127-0a2e-4c5b-9a4a-85680f60eab8",
            },
            master_password="password123",
            network="base-sepolia",
            to={"address": "0x2FD2ed754fCD8748b89D5577241E76432306D5a5"},
        )
        assert_matches_type(TransferCreateResponse, transfer, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncVvallet) -> None:
        response = await async_client.transfer.with_raw_response.create(
            amount=1,
            from_={
                "address": "0xF1C7ee435E5e46C3CCef62c1eE21f97dEfe9816A",
                "wallet_id": "4a65b127-0a2e-4c5b-9a4a-85680f60eab8",
            },
            master_password="password123",
            network="base-sepolia",
            to={"address": "0x2FD2ed754fCD8748b89D5577241E76432306D5a5"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transfer = await response.parse()
        assert_matches_type(TransferCreateResponse, transfer, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncVvallet) -> None:
        async with async_client.transfer.with_streaming_response.create(
            amount=1,
            from_={
                "address": "0xF1C7ee435E5e46C3CCef62c1eE21f97dEfe9816A",
                "wallet_id": "4a65b127-0a2e-4c5b-9a4a-85680f60eab8",
            },
            master_password="password123",
            network="base-sepolia",
            to={"address": "0x2FD2ed754fCD8748b89D5577241E76432306D5a5"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transfer = await response.parse()
            assert_matches_type(TransferCreateResponse, transfer, path=["response"])

        assert cast(Any, response.is_closed) is True
