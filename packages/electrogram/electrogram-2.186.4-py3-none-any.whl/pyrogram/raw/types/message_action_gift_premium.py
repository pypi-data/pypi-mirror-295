from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class MessageActionGiftPremium(TLObject):  # type: ignore
    """Info about a gifted Telegram Premium subscription

    Constructor of :obj:`~pyrogram.raw.base.MessageAction`.

    Details:
        - Layer: ``187``
        - ID: ``C83D6AEC``

    Parameters:
        currency (``str``):
            Three-letter ISO 4217 currency code

        amount (``int`` ``64-bit``):
            Price of the gift in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).

        months (``int`` ``32-bit``):
            Duration of the gifted Telegram Premium subscription

        crypto_currency (``str``, *optional*):
            If the gift was bought using a cryptocurrency, the cryptocurrency name.

        crypto_amount (``int`` ``64-bit``, *optional*):
            If the gift was bought using a cryptocurrency, price of the gift in the smallest units of a cryptocurrency.

    """

    __slots__: List[str] = ["currency", "amount", "months", "crypto_currency", "crypto_amount"]

    ID = 0xc83d6aec
    QUALNAME = "types.MessageActionGiftPremium"

    def __init__(self, *, currency: str, amount: int, months: int, crypto_currency: Optional[str] = None, crypto_amount: Optional[int] = None) -> None:
        self.currency = currency  # string
        self.amount = amount  # long
        self.months = months  # int
        self.crypto_currency = crypto_currency  # flags.0?string
        self.crypto_amount = crypto_amount  # flags.0?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionGiftPremium":
        
        flags = Int.read(b)
        
        currency = String.read(b)
        
        amount = Long.read(b)
        
        months = Int.read(b)
        
        crypto_currency = String.read(b) if flags & (1 << 0) else None
        crypto_amount = Long.read(b) if flags & (1 << 0) else None
        return MessageActionGiftPremium(currency=currency, amount=amount, months=months, crypto_currency=crypto_currency, crypto_amount=crypto_amount)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.crypto_currency is not None else 0
        flags |= (1 << 0) if self.crypto_amount is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.currency))
        
        b.write(Long(self.amount))
        
        b.write(Int(self.months))
        
        if self.crypto_currency is not None:
            b.write(String(self.crypto_currency))
        
        if self.crypto_amount is not None:
            b.write(Long(self.crypto_amount))
        
        return b.getvalue()
