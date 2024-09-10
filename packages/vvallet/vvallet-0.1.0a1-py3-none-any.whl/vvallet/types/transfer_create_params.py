# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TransferCreateParams", "From", "To"]


class TransferCreateParams(TypedDict, total=False):
    amount: Required[float]
    """The amount of the transfer"""

    from_: Required[Annotated[From, PropertyInfo(alias="from")]]

    master_password: Required[Annotated[str, PropertyInfo(alias="masterPassword")]]
    """The master password of the user."""

    network: Required[
        Literal["base-sepolia", "base-mainnet", "ethereum-holesky", "ethereum-mainnet", "polygon-mainnet"]
    ]
    """The network id"""

    to: Required[To]


class From(TypedDict, total=False):
    address: Required[str]
    """The address of the wallet"""

    wallet_id: Required[Annotated[str, PropertyInfo(alias="walletId")]]
    """The wallet id"""


class To(TypedDict, total=False):
    address: Required[str]
    """The address of the wallet"""
