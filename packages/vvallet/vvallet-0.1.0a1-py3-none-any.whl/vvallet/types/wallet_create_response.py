# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from .._models import BaseModel

__all__ = ["WalletCreateResponse", "Wallet", "WalletAddress"]


class WalletAddress(BaseModel):
    id: str
    """The default address of the newly created wallet"""


class Wallet(BaseModel):
    id: str
    """The unique identifier of the newly created wallet"""

    address: WalletAddress


class WalletCreateResponse(BaseModel):
    wallet: Wallet
