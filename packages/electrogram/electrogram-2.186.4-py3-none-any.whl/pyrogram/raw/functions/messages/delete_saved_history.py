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


class DeleteSavedHistory(TLObject):  # type: ignore
    """Deletes messages forwarded from a specific peer to saved messages ».


    Details:
        - Layer: ``187``
        - ID: ``6E98102B``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            Peer, whose messages will be deleted from saved messages »

        max_id (``int`` ``32-bit``):
            Maximum ID of message to delete

        min_date (``int`` ``32-bit``, *optional*):
            Delete all messages newer than this UNIX timestamp

        max_date (``int`` ``32-bit``, *optional*):
            Delete all messages older than this UNIX timestamp

    Returns:
        :obj:`messages.AffectedHistory <pyrogram.raw.base.messages.AffectedHistory>`
    """

    __slots__: List[str] = ["peer", "max_id", "min_date", "max_date"]

    ID = 0x6e98102b
    QUALNAME = "functions.messages.DeleteSavedHistory"

    def __init__(self, *, peer: "raw.base.InputPeer", max_id: int, min_date: Optional[int] = None, max_date: Optional[int] = None) -> None:
        self.peer = peer  # InputPeer
        self.max_id = max_id  # int
        self.min_date = min_date  # flags.2?int
        self.max_date = max_date  # flags.3?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DeleteSavedHistory":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        max_id = Int.read(b)
        
        min_date = Int.read(b) if flags & (1 << 2) else None
        max_date = Int.read(b) if flags & (1 << 3) else None
        return DeleteSavedHistory(peer=peer, max_id=max_id, min_date=min_date, max_date=max_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.min_date is not None else 0
        flags |= (1 << 3) if self.max_date is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.max_id))
        
        if self.min_date is not None:
            b.write(Int(self.min_date))
        
        if self.max_date is not None:
            b.write(Int(self.max_date))
        
        return b.getvalue()
