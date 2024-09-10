# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import transfer_create_params
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
from ..types.transfer_create_response import TransferCreateResponse

__all__ = ["TransferResource", "AsyncTransferResource"]


class TransferResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TransferResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/li2109/vvallet-python#accessing-raw-response-data-eg-headers
        """
        return TransferResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TransferResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/li2109/vvallet-python#with_streaming_response
        """
        return TransferResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        amount: float,
        from_: transfer_create_params.From,
        master_password: str,
        network: Literal["base-sepolia", "base-mainnet", "ethereum-holesky", "ethereum-mainnet", "polygon-mainnet"],
        to: transfer_create_params.To,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransferCreateResponse:
        """
        Transfer funds from one wallet or address to another

        Args:
          amount: The amount of the transfer

          master_password: The master password of the user.

          network: The network id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/transfer",
            body=maybe_transform(
                {
                    "amount": amount,
                    "from_": from_,
                    "master_password": master_password,
                    "network": network,
                    "to": to,
                },
                transfer_create_params.TransferCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransferCreateResponse,
        )


class AsyncTransferResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTransferResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/li2109/vvallet-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTransferResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTransferResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/li2109/vvallet-python#with_streaming_response
        """
        return AsyncTransferResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        amount: float,
        from_: transfer_create_params.From,
        master_password: str,
        network: Literal["base-sepolia", "base-mainnet", "ethereum-holesky", "ethereum-mainnet", "polygon-mainnet"],
        to: transfer_create_params.To,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransferCreateResponse:
        """
        Transfer funds from one wallet or address to another

        Args:
          amount: The amount of the transfer

          master_password: The master password of the user.

          network: The network id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/transfer",
            body=await async_maybe_transform(
                {
                    "amount": amount,
                    "from_": from_,
                    "master_password": master_password,
                    "network": network,
                    "to": to,
                },
                transfer_create_params.TransferCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransferCreateResponse,
        )


class TransferResourceWithRawResponse:
    def __init__(self, transfer: TransferResource) -> None:
        self._transfer = transfer

        self.create = to_raw_response_wrapper(
            transfer.create,
        )


class AsyncTransferResourceWithRawResponse:
    def __init__(self, transfer: AsyncTransferResource) -> None:
        self._transfer = transfer

        self.create = async_to_raw_response_wrapper(
            transfer.create,
        )


class TransferResourceWithStreamingResponse:
    def __init__(self, transfer: TransferResource) -> None:
        self._transfer = transfer

        self.create = to_streamed_response_wrapper(
            transfer.create,
        )


class AsyncTransferResourceWithStreamingResponse:
    def __init__(self, transfer: AsyncTransferResource) -> None:
        self._transfer = transfer

        self.create = async_to_streamed_response_wrapper(
            transfer.create,
        )
