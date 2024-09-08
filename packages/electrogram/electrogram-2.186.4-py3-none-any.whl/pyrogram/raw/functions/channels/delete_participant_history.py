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


class DeleteParticipantHistory(TLObject):  # type: ignore
    """Delete all messages sent by a specific participant of a given supergroup


    Details:
        - Layer: ``187``
        - ID: ``367544DB``

    Parameters:
        channel (:obj:`InputChannel <pyrogram.raw.base.InputChannel>`):
            Supergroup

        participant (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            The participant whose messages should be deleted

    Returns:
        :obj:`messages.AffectedHistory <pyrogram.raw.base.messages.AffectedHistory>`
    """

    __slots__: List[str] = ["channel", "participant"]

    ID = 0x367544db
    QUALNAME = "functions.channels.DeleteParticipantHistory"

    def __init__(self, *, channel: "raw.base.InputChannel", participant: "raw.base.InputPeer") -> None:
        self.channel = channel  # InputChannel
        self.participant = participant  # InputPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DeleteParticipantHistory":
        # No flags
        
        channel = TLObject.read(b)
        
        participant = TLObject.read(b)
        
        return DeleteParticipantHistory(channel=channel, participant=participant)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(self.participant.write())
        
        return b.getvalue()
