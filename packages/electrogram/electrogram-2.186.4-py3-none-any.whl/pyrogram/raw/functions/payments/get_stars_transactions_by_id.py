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


class GetStarsTransactionsByID(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``187``
        - ID: ``27842D2E``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        id (List of :obj:`InputStarsTransaction <pyrogram.raw.base.InputStarsTransaction>`):
            N/A

    Returns:
        :obj:`payments.StarsStatus <pyrogram.raw.base.payments.StarsStatus>`
    """

    __slots__: List[str] = ["peer", "id"]

    ID = 0x27842d2e
    QUALNAME = "functions.payments.GetStarsTransactionsByID"

    def __init__(self, *, peer: "raw.base.InputPeer", id: List["raw.base.InputStarsTransaction"]) -> None:
        self.peer = peer  # InputPeer
        self.id = id  # Vector<InputStarsTransaction>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetStarsTransactionsByID":
        # No flags
        
        peer = TLObject.read(b)
        
        id = TLObject.read(b)
        
        return GetStarsTransactionsByID(peer=peer, id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Vector(self.id))
        
        return b.getvalue()
