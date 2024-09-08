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


class EditPhoto(TLObject):  # type: ignore
    """Change the photo of a channel/supergroup


    Details:
        - Layer: ``187``
        - ID: ``F12E57C9``

    Parameters:
        channel (:obj:`InputChannel <pyrogram.raw.base.InputChannel>`):
            Channel/supergroup whose photo should be edited

        photo (:obj:`InputChatPhoto <pyrogram.raw.base.InputChatPhoto>`):
            New photo

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["channel", "photo"]

    ID = 0xf12e57c9
    QUALNAME = "functions.channels.EditPhoto"

    def __init__(self, *, channel: "raw.base.InputChannel", photo: "raw.base.InputChatPhoto") -> None:
        self.channel = channel  # InputChannel
        self.photo = photo  # InputChatPhoto

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditPhoto":
        # No flags
        
        channel = TLObject.read(b)
        
        photo = TLObject.read(b)
        
        return EditPhoto(channel=channel, photo=photo)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(self.photo.write())
        
        return b.getvalue()
