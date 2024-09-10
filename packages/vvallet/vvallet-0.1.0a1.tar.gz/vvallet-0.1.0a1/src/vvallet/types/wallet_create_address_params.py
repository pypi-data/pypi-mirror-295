# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["WalletCreateAddressParams"]


class WalletCreateAddressParams(TypedDict, total=False):
    master_password: Required[Annotated[str, PropertyInfo(alias="masterPassword")]]
    """The master password of the user."""

    wallet_id: Required[Annotated[str, PropertyInfo(alias="walletId")]]
    """The wallet id"""
