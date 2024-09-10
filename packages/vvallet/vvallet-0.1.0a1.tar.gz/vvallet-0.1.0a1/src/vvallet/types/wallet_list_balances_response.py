# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict

from .._models import BaseModel

__all__ = ["WalletListBalancesResponse", "Wallet"]


class Wallet(BaseModel):
    id: str
    """The unique identifier of the wallet"""

    balances: Dict[str, float]
    """The balances of the wallet keyed by the asset id"""


class WalletListBalancesResponse(BaseModel):
    wallet: Wallet
