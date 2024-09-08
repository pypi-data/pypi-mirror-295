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


class ChannelParticipantsContacts(TLObject):  # type: ignore
    """Fetch only participants that are also contacts

    Constructor of :obj:`~pyrogram.raw.base.ChannelParticipantsFilter`.

    Details:
        - Layer: ``187``
        - ID: ``BB6AE88D``

    Parameters:
        q (``str``):
            Optional search query for searching contact participants by name

    """

    __slots__: List[str] = ["q"]

    ID = 0xbb6ae88d
    QUALNAME = "types.ChannelParticipantsContacts"

    def __init__(self, *, q: str) -> None:
        self.q = q  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelParticipantsContacts":
        # No flags
        
        q = String.read(b)
        
        return ChannelParticipantsContacts(q=q)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.q))
        
        return b.getvalue()
