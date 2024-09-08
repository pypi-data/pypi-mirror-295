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


class SendMessageRecordAudioAction(TLObject):  # type: ignore
    """User is recording a voice message.

    Constructor of :obj:`~pyrogram.raw.base.SendMessageAction`.

    Details:
        - Layer: ``187``
        - ID: ``D52F73F7``

    Parameters:
        No parameters required.

    """

    __slots__: List[str] = []

    ID = 0xd52f73f7
    QUALNAME = "types.SendMessageRecordAudioAction"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendMessageRecordAudioAction":
        # No flags
        
        return SendMessageRecordAudioAction()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
