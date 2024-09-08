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


class ForwardMessages(TLObject):  # type: ignore
    """Forwards messages by their IDs.


    Details:
        - Layer: ``187``
        - ID: ``D5039208``

    Parameters:
        from_peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            Source of messages

        id (List of ``int`` ``32-bit``):
            IDs of messages

        random_id (List of ``int`` ``64-bit``):
            Random ID to prevent resending of messages

        to_peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            Destination peer

        silent (``bool``, *optional*):
            Whether to send messages silently (no notification will be triggered on the destination clients)

        background (``bool``, *optional*):
            Whether to send the message in background

        with_my_score (``bool``, *optional*):
            When forwarding games, whether to include your score in the game

        drop_author (``bool``, *optional*):
            Whether to forward messages without quoting the original author

        drop_media_captions (``bool``, *optional*):
            Whether to strip captions from media

        noforwards (``bool``, *optional*):
            Only for bots, disallows further re-forwarding and saving of the messages, even if the destination chat doesn't have content protection enabled

        top_msg_id (``int`` ``32-bit``, *optional*):
            Destination forum topic

        schedule_date (``int`` ``32-bit``, *optional*):
            Scheduled message date for scheduled messages

        send_as (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`, *optional*):
            Forward the messages as the specified peer

        quick_reply_shortcut (:obj:`InputQuickReplyShortcut <pyrogram.raw.base.InputQuickReplyShortcut>`, *optional*):
            

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["from_peer", "id", "random_id", "to_peer", "silent", "background", "with_my_score", "drop_author", "drop_media_captions", "noforwards", "top_msg_id", "schedule_date", "send_as", "quick_reply_shortcut"]

    ID = 0xd5039208
    QUALNAME = "functions.messages.ForwardMessages"

    def __init__(self, *, from_peer: "raw.base.InputPeer", id: List[int], random_id: List[int], to_peer: "raw.base.InputPeer", silent: Optional[bool] = None, background: Optional[bool] = None, with_my_score: Optional[bool] = None, drop_author: Optional[bool] = None, drop_media_captions: Optional[bool] = None, noforwards: Optional[bool] = None, top_msg_id: Optional[int] = None, schedule_date: Optional[int] = None, send_as: "raw.base.InputPeer" = None, quick_reply_shortcut: "raw.base.InputQuickReplyShortcut" = None) -> None:
        self.from_peer = from_peer  # InputPeer
        self.id = id  # Vector<int>
        self.random_id = random_id  # Vector<long>
        self.to_peer = to_peer  # InputPeer
        self.silent = silent  # flags.5?true
        self.background = background  # flags.6?true
        self.with_my_score = with_my_score  # flags.8?true
        self.drop_author = drop_author  # flags.11?true
        self.drop_media_captions = drop_media_captions  # flags.12?true
        self.noforwards = noforwards  # flags.14?true
        self.top_msg_id = top_msg_id  # flags.9?int
        self.schedule_date = schedule_date  # flags.10?int
        self.send_as = send_as  # flags.13?InputPeer
        self.quick_reply_shortcut = quick_reply_shortcut  # flags.17?InputQuickReplyShortcut

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ForwardMessages":
        
        flags = Int.read(b)
        
        silent = True if flags & (1 << 5) else False
        background = True if flags & (1 << 6) else False
        with_my_score = True if flags & (1 << 8) else False
        drop_author = True if flags & (1 << 11) else False
        drop_media_captions = True if flags & (1 << 12) else False
        noforwards = True if flags & (1 << 14) else False
        from_peer = TLObject.read(b)
        
        id = TLObject.read(b, Int)
        
        random_id = TLObject.read(b, Long)
        
        to_peer = TLObject.read(b)
        
        top_msg_id = Int.read(b) if flags & (1 << 9) else None
        schedule_date = Int.read(b) if flags & (1 << 10) else None
        send_as = TLObject.read(b) if flags & (1 << 13) else None
        
        quick_reply_shortcut = TLObject.read(b) if flags & (1 << 17) else None
        
        return ForwardMessages(from_peer=from_peer, id=id, random_id=random_id, to_peer=to_peer, silent=silent, background=background, with_my_score=with_my_score, drop_author=drop_author, drop_media_captions=drop_media_captions, noforwards=noforwards, top_msg_id=top_msg_id, schedule_date=schedule_date, send_as=send_as, quick_reply_shortcut=quick_reply_shortcut)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 5) if self.silent else 0
        flags |= (1 << 6) if self.background else 0
        flags |= (1 << 8) if self.with_my_score else 0
        flags |= (1 << 11) if self.drop_author else 0
        flags |= (1 << 12) if self.drop_media_captions else 0
        flags |= (1 << 14) if self.noforwards else 0
        flags |= (1 << 9) if self.top_msg_id is not None else 0
        flags |= (1 << 10) if self.schedule_date is not None else 0
        flags |= (1 << 13) if self.send_as is not None else 0
        flags |= (1 << 17) if self.quick_reply_shortcut is not None else 0
        b.write(Int(flags))
        
        b.write(self.from_peer.write())
        
        b.write(Vector(self.id, Int))
        
        b.write(Vector(self.random_id, Long))
        
        b.write(self.to_peer.write())
        
        if self.top_msg_id is not None:
            b.write(Int(self.top_msg_id))
        
        if self.schedule_date is not None:
            b.write(Int(self.schedule_date))
        
        if self.send_as is not None:
            b.write(self.send_as.write())
        
        if self.quick_reply_shortcut is not None:
            b.write(self.quick_reply_shortcut.write())
        
        return b.getvalue()
