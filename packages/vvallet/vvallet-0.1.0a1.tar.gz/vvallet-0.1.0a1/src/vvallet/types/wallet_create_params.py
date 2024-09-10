# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["WalletCreateParams"]


class WalletCreateParams(TypedDict, total=False):
    master_password: Required[Annotated[str, PropertyInfo(alias="masterPassword")]]
    """The master password used to encrypt the wallet seed.

    Not stored in the database and only known to the user.
    """

    network: Required[
        Literal["base-sepolia", "base-mainnet", "ethereum-holesky", "ethereum-mainnet", "polygon-mainnet"]
    ]
    """The network on which the wallet will be created.

    Testnet will be faucet with ETH and USDC.
    """
