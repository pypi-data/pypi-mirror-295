# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import (
    wallet_create_params,
    wallet_list_balances_params,
    wallet_create_address_params,
    wallet_list_addresses_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.wallet_create_response import WalletCreateResponse
from ..types.wallet_list_balances_response import WalletListBalancesResponse
from ..types.wallet_create_address_response import WalletCreateAddressResponse
from ..types.wallet_list_addresses_response import WalletListAddressesResponse

__all__ = ["WalletResource", "AsyncWalletResource"]


class WalletResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WalletResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/li2109/vvallet-python#accessing-raw-response-data-eg-headers
        """
        return WalletResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WalletResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/li2109/vvallet-python#with_streaming_response
        """
        return WalletResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        master_password: str,
        network: Literal["base-sepolia", "base-mainnet", "ethereum-holesky", "ethereum-mainnet", "polygon-mainnet"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WalletCreateResponse:
        """
        Create a new wallet

        Args:
          master_password: The master password used to encrypt the wallet seed. Not stored in the database
              and only known to the user.

          network: The network on which the wallet will be created. Testnet will be faucet with ETH
              and USDC.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/createWallet",
            body=maybe_transform(
                {
                    "master_password": master_password,
                    "network": network,
                },
                wallet_create_params.WalletCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WalletCreateResponse,
        )

    def create_address(
        self,
        *,
        master_password: str,
        wallet_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WalletCreateAddressResponse:
        """
        Create a new address to a wallet

        Args:
          master_password: The master password of the user.

          wallet_id: The wallet id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/createAddress",
            body=maybe_transform(
                {
                    "master_password": master_password,
                    "wallet_id": wallet_id,
                },
                wallet_create_address_params.WalletCreateAddressParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WalletCreateAddressResponse,
        )

    def list_addresses(
        self,
        *,
        wallet_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WalletListAddressesResponse:
        """
        List all addresses of a wallet

        Args:
          wallet_id: The unique identifier of the wallet

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/listAddress",
            body=maybe_transform({"wallet_id": wallet_id}, wallet_list_addresses_params.WalletListAddressesParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WalletListAddressesResponse,
        )

    def list_balances(
        self,
        *,
        wallet_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WalletListBalancesResponse:
        """
        List all balances of a wallet

        Args:
          wallet_id: The unique identifier of the wallet

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/listBalances",
            body=maybe_transform({"wallet_id": wallet_id}, wallet_list_balances_params.WalletListBalancesParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WalletListBalancesResponse,
        )


class AsyncWalletResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWalletResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/li2109/vvallet-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWalletResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWalletResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/li2109/vvallet-python#with_streaming_response
        """
        return AsyncWalletResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        master_password: str,
        network: Literal["base-sepolia", "base-mainnet", "ethereum-holesky", "ethereum-mainnet", "polygon-mainnet"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WalletCreateResponse:
        """
        Create a new wallet

        Args:
          master_password: The master password used to encrypt the wallet seed. Not stored in the database
              and only known to the user.

          network: The network on which the wallet will be created. Testnet will be faucet with ETH
              and USDC.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/createWallet",
            body=await async_maybe_transform(
                {
                    "master_password": master_password,
                    "network": network,
                },
                wallet_create_params.WalletCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WalletCreateResponse,
        )

    async def create_address(
        self,
        *,
        master_password: str,
        wallet_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WalletCreateAddressResponse:
        """
        Create a new address to a wallet

        Args:
          master_password: The master password of the user.

          wallet_id: The wallet id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/createAddress",
            body=await async_maybe_transform(
                {
                    "master_password": master_password,
                    "wallet_id": wallet_id,
                },
                wallet_create_address_params.WalletCreateAddressParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WalletCreateAddressResponse,
        )

    async def list_addresses(
        self,
        *,
        wallet_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WalletListAddressesResponse:
        """
        List all addresses of a wallet

        Args:
          wallet_id: The unique identifier of the wallet

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/listAddress",
            body=await async_maybe_transform(
                {"wallet_id": wallet_id}, wallet_list_addresses_params.WalletListAddressesParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WalletListAddressesResponse,
        )

    async def list_balances(
        self,
        *,
        wallet_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WalletListBalancesResponse:
        """
        List all balances of a wallet

        Args:
          wallet_id: The unique identifier of the wallet

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/listBalances",
            body=await async_maybe_transform(
                {"wallet_id": wallet_id}, wallet_list_balances_params.WalletListBalancesParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WalletListBalancesResponse,
        )


class WalletResourceWithRawResponse:
    def __init__(self, wallet: WalletResource) -> None:
        self._wallet = wallet

        self.create = to_raw_response_wrapper(
            wallet.create,
        )
        self.create_address = to_raw_response_wrapper(
            wallet.create_address,
        )
        self.list_addresses = to_raw_response_wrapper(
            wallet.list_addresses,
        )
        self.list_balances = to_raw_response_wrapper(
            wallet.list_balances,
        )


class AsyncWalletResourceWithRawResponse:
    def __init__(self, wallet: AsyncWalletResource) -> None:
        self._wallet = wallet

        self.create = async_to_raw_response_wrapper(
            wallet.create,
        )
        self.create_address = async_to_raw_response_wrapper(
            wallet.create_address,
        )
        self.list_addresses = async_to_raw_response_wrapper(
            wallet.list_addresses,
        )
        self.list_balances = async_to_raw_response_wrapper(
            wallet.list_balances,
        )


class WalletResourceWithStreamingResponse:
    def __init__(self, wallet: WalletResource) -> None:
        self._wallet = wallet

        self.create = to_streamed_response_wrapper(
            wallet.create,
        )
        self.create_address = to_streamed_response_wrapper(
            wallet.create_address,
        )
        self.list_addresses = to_streamed_response_wrapper(
            wallet.list_addresses,
        )
        self.list_balances = to_streamed_response_wrapper(
            wallet.list_balances,
        )


class AsyncWalletResourceWithStreamingResponse:
    def __init__(self, wallet: AsyncWalletResource) -> None:
        self._wallet = wallet

        self.create = async_to_streamed_response_wrapper(
            wallet.create,
        )
        self.create_address = async_to_streamed_response_wrapper(
            wallet.create_address,
        )
        self.list_addresses = async_to_streamed_response_wrapper(
            wallet.list_addresses,
        )
        self.list_balances = async_to_streamed_response_wrapper(
            wallet.list_balances,
        )
