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


class Report(TLObject):  # type: ignore
    """Report a message in a chat for violation of telegram's Terms of Service


    Details:
        - Layer: ``187``
        - ID: ``8953AB4E``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            Peer

        id (List of ``int`` ``32-bit``):
            IDs of messages to report

        reason (:obj:`ReportReason <pyrogram.raw.base.ReportReason>`):
            Why are these messages being reported

        message (``str``):
            Comment for report moderation

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["peer", "id", "reason", "message"]

    ID = 0x8953ab4e
    QUALNAME = "functions.messages.Report"

    def __init__(self, *, peer: "raw.base.InputPeer", id: List[int], reason: "raw.base.ReportReason", message: str) -> None:
        self.peer = peer  # InputPeer
        self.id = id  # Vector<int>
        self.reason = reason  # ReportReason
        self.message = message  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Report":
        # No flags
        
        peer = TLObject.read(b)
        
        id = TLObject.read(b, Int)
        
        reason = TLObject.read(b)
        
        message = String.read(b)
        
        return Report(peer=peer, id=id, reason=reason, message=message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Vector(self.id, Int))
        
        b.write(self.reason.write())
        
        b.write(String(self.message))
        
        return b.getvalue()
