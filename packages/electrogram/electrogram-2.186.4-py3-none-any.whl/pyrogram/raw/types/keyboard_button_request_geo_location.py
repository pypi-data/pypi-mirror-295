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


class KeyboardButtonRequestGeoLocation(TLObject):  # type: ignore
    """Button to request a user's geolocation

    Constructor of :obj:`~pyrogram.raw.base.KeyboardButton`.

    Details:
        - Layer: ``187``
        - ID: ``FC796B3F``

    Parameters:
        text (``str``):
            Button text

    """

    __slots__: List[str] = ["text"]

    ID = 0xfc796b3f
    QUALNAME = "types.KeyboardButtonRequestGeoLocation"

    def __init__(self, *, text: str) -> None:
        self.text = text  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "KeyboardButtonRequestGeoLocation":
        # No flags
        
        text = String.read(b)
        
        return KeyboardButtonRequestGeoLocation(text=text)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.text))
        
        return b.getvalue()
