# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.



from .._models import BaseModel

__all__ = ["TransferCreateResponse", "Transaction"]


class Transaction(BaseModel):
    hash: str
    """The transaction id"""

    link: str
    """The transaction link"""


class TransferCreateResponse(BaseModel):
    transaction: Transaction
