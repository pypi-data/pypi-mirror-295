# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["WalletListAddressesResponse", "Wallet"]


class Wallet(BaseModel):
    id: str
    """The unique identifier of the wallet"""

    address: List[str]
    """An array of all addresses associated with the wallet"""


class WalletListAddressesResponse(BaseModel):
    wallet: Wallet
