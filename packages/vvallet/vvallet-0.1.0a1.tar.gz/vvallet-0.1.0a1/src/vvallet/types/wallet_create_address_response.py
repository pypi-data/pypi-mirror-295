# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["WalletCreateAddressResponse", "Wallet"]


class Wallet(BaseModel):
    id: str
    """The wallet id"""

    address: List[str]
    """All addresses(including the new one) of the wallet"""


class WalletCreateAddressResponse(BaseModel):
    wallet: Wallet
