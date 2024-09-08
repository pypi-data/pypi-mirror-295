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


class EmojiStatusUntil(TLObject):  # type: ignore
    """An emoji status valid until the specified date

    Constructor of :obj:`~pyrogram.raw.base.EmojiStatus`.

    Details:
        - Layer: ``187``
        - ID: ``FA30A8C7``

    Parameters:
        document_id (``int`` ``64-bit``):
            Custom emoji document ID

        until (``int`` ``32-bit``):
            This status is valid until this date

    """

    __slots__: List[str] = ["document_id", "until"]

    ID = 0xfa30a8c7
    QUALNAME = "types.EmojiStatusUntil"

    def __init__(self, *, document_id: int, until: int) -> None:
        self.document_id = document_id  # long
        self.until = until  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EmojiStatusUntil":
        # No flags
        
        document_id = Long.read(b)
        
        until = Int.read(b)
        
        return EmojiStatusUntil(document_id=document_id, until=until)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.document_id))
        
        b.write(Int(self.until))
        
        return b.getvalue()
