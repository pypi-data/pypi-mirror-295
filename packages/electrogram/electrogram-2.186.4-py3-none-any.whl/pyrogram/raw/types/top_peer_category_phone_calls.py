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


class TopPeerCategoryPhoneCalls(TLObject):  # type: ignore
    """Most frequently called users

    Constructor of :obj:`~pyrogram.raw.base.TopPeerCategory`.

    Details:
        - Layer: ``187``
        - ID: ``1E76A78C``

    Parameters:
        No parameters required.

    """

    __slots__: List[str] = []

    ID = 0x1e76a78c
    QUALNAME = "types.TopPeerCategoryPhoneCalls"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TopPeerCategoryPhoneCalls":
        # No flags
        
        return TopPeerCategoryPhoneCalls()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
