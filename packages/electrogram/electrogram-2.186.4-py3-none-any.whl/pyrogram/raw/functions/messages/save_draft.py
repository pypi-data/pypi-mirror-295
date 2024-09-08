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


class SaveDraft(TLObject):  # type: ignore
    """Save a message draft associated to a chat.


    Details:
        - Layer: ``187``
        - ID: ``D372C5CE``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            Destination of the message that should be sent

        message (``str``):
            The draft

        no_webpage (``bool``, *optional*):
            Disable generation of the webpage preview

        invert_media (``bool``, *optional*):
            If set, any eventual webpage preview will be shown on top of the message instead of at the bottom.

        reply_to (:obj:`InputReplyTo <pyrogram.raw.base.InputReplyTo>`, *optional*):
            If set, indicates that the message should be sent in reply to the specified message or story.

        entities (List of :obj:`MessageEntity <pyrogram.raw.base.MessageEntity>`, *optional*):
            Message entities for styled text

        media (:obj:`InputMedia <pyrogram.raw.base.InputMedia>`, *optional*):
            Attached media

        effect (``int`` ``64-bit``, *optional*):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["peer", "message", "no_webpage", "invert_media", "reply_to", "entities", "media", "effect"]

    ID = 0xd372c5ce
    QUALNAME = "functions.messages.SaveDraft"

    def __init__(self, *, peer: "raw.base.InputPeer", message: str, no_webpage: Optional[bool] = None, invert_media: Optional[bool] = None, reply_to: "raw.base.InputReplyTo" = None, entities: Optional[List["raw.base.MessageEntity"]] = None, media: "raw.base.InputMedia" = None, effect: Optional[int] = None) -> None:
        self.peer = peer  # InputPeer
        self.message = message  # string
        self.no_webpage = no_webpage  # flags.1?true
        self.invert_media = invert_media  # flags.6?true
        self.reply_to = reply_to  # flags.4?InputReplyTo
        self.entities = entities  # flags.3?Vector<MessageEntity>
        self.media = media  # flags.5?InputMedia
        self.effect = effect  # flags.7?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SaveDraft":
        
        flags = Int.read(b)
        
        no_webpage = True if flags & (1 << 1) else False
        invert_media = True if flags & (1 << 6) else False
        reply_to = TLObject.read(b) if flags & (1 << 4) else None
        
        peer = TLObject.read(b)
        
        message = String.read(b)
        
        entities = TLObject.read(b) if flags & (1 << 3) else []
        
        media = TLObject.read(b) if flags & (1 << 5) else None
        
        effect = Long.read(b) if flags & (1 << 7) else None
        return SaveDraft(peer=peer, message=message, no_webpage=no_webpage, invert_media=invert_media, reply_to=reply_to, entities=entities, media=media, effect=effect)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.no_webpage else 0
        flags |= (1 << 6) if self.invert_media else 0
        flags |= (1 << 4) if self.reply_to is not None else 0
        flags |= (1 << 3) if self.entities else 0
        flags |= (1 << 5) if self.media is not None else 0
        flags |= (1 << 7) if self.effect is not None else 0
        b.write(Int(flags))
        
        if self.reply_to is not None:
            b.write(self.reply_to.write())
        
        b.write(self.peer.write())
        
        b.write(String(self.message))
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        if self.media is not None:
            b.write(self.media.write())
        
        if self.effect is not None:
            b.write(Long(self.effect))
        
        return b.getvalue()
