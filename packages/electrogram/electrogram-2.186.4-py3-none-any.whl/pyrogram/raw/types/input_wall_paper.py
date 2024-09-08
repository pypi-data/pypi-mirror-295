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


class InputWallPaper(TLObject):  # type: ignore
    """Wallpaper

    Constructor of :obj:`~pyrogram.raw.base.InputWallPaper`.

    Details:
        - Layer: ``187``
        - ID: ``E630B979``

    Parameters:
        id (``int`` ``64-bit``):
            Wallpaper ID

        access_hash (``int`` ``64-bit``):
            Access hash

    """

    __slots__: List[str] = ["id", "access_hash"]

    ID = 0xe630b979
    QUALNAME = "types.InputWallPaper"

    def __init__(self, *, id: int, access_hash: int) -> None:
        self.id = id  # long
        self.access_hash = access_hash  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputWallPaper":
        # No flags
        
        id = Long.read(b)
        
        access_hash = Long.read(b)
        
        return InputWallPaper(id=id, access_hash=access_hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.id))
        
        b.write(Long(self.access_hash))
        
        return b.getvalue()
