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


class SponsoredMessages(TLObject):  # type: ignore
    """A set of sponsored messages associated to a channel

    Constructor of :obj:`~pyrogram.raw.base.messages.SponsoredMessages`.

    Details:
        - Layer: ``187``
        - ID: ``C9EE1D87``

    Parameters:
        messages (List of :obj:`SponsoredMessage <pyrogram.raw.base.SponsoredMessage>`):
            Sponsored messages

        chats (List of :obj:`Chat <pyrogram.raw.base.Chat>`):
            Chats mentioned in the sponsored messages

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            Users mentioned in the sponsored messages

        posts_between (``int`` ``32-bit``, *optional*):
            If set, specifies the minimum number of messages between shown sponsored messages; otherwise, only one sponsored message must be shown after all ordinary messages.

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            channels.GetSponsoredMessages
    """

    __slots__: List[str] = ["messages", "chats", "users", "posts_between"]

    ID = 0xc9ee1d87
    QUALNAME = "types.messages.SponsoredMessages"

    def __init__(self, *, messages: List["raw.base.SponsoredMessage"], chats: List["raw.base.Chat"], users: List["raw.base.User"], posts_between: Optional[int] = None) -> None:
        self.messages = messages  # Vector<SponsoredMessage>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.posts_between = posts_between  # flags.0?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SponsoredMessages":
        
        flags = Int.read(b)
        
        posts_between = Int.read(b) if flags & (1 << 0) else None
        messages = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return SponsoredMessages(messages=messages, chats=chats, users=users, posts_between=posts_between)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.posts_between is not None else 0
        b.write(Int(flags))
        
        if self.posts_between is not None:
            b.write(Int(self.posts_between))
        
        b.write(Vector(self.messages))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
