# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["WalletListBalancesParams"]


class WalletListBalancesParams(TypedDict, total=False):
    wallet_id: Required[Annotated[str, PropertyInfo(alias="walletId")]]
    """The unique identifier of the wallet"""
