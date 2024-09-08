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


class TranscribeAudio(TLObject):  # type: ignore
    """Transcribe voice message


    Details:
        - Layer: ``187``
        - ID: ``269E9A49``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            Peer ID where the voice message was sent

        msg_id (``int`` ``32-bit``):
            Voice message ID

    Returns:
        :obj:`messages.TranscribedAudio <pyrogram.raw.base.messages.TranscribedAudio>`
    """

    __slots__: List[str] = ["peer", "msg_id"]

    ID = 0x269e9a49
    QUALNAME = "functions.messages.TranscribeAudio"

    def __init__(self, *, peer: "raw.base.InputPeer", msg_id: int) -> None:
        self.peer = peer  # InputPeer
        self.msg_id = msg_id  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TranscribeAudio":
        # No flags
        
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        return TranscribeAudio(peer=peer, msg_id=msg_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        return b.getvalue()
