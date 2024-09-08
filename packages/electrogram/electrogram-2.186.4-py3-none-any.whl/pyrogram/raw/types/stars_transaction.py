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


class StarsTransaction(TLObject):  # type: ignore
    """{schema}

    Constructor of :obj:`~pyrogram.raw.base.StarsTransaction`.

    Details:
        - Layer: ``187``
        - ID: ``EE7522D5``

    Parameters:
        id (``str``):
            

        stars (``int`` ``64-bit``):
            

        date (``int`` ``32-bit``):
            

        peer (:obj:`StarsTransactionPeer <pyrogram.raw.base.StarsTransactionPeer>`):
            

        refund (``bool``, *optional*):
            

        pending (``bool``, *optional*):
            N/A

        failed (``bool``, *optional*):
            N/A

        gift (``bool``, *optional*):
            N/A

        reaction (``bool``, *optional*):
            N/A

        title (``str``, *optional*):
            

        description (``str``, *optional*):
            

        photo (:obj:`WebDocument <pyrogram.raw.base.WebDocument>`, *optional*):
            

        transaction_date (``int`` ``32-bit``, *optional*):
            N/A

        transaction_url (``str``, *optional*):
            N/A

        bot_payload (``bytes``, *optional*):
            N/A

        msg_id (``int`` ``32-bit``, *optional*):
            N/A

        extended_media (List of :obj:`MessageMedia <pyrogram.raw.base.MessageMedia>`, *optional*):
            N/A

        subscription_period (``int`` ``32-bit``, *optional*):
            N/A

        giveaway_post_id (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "stars", "date", "peer", "refund", "pending", "failed", "gift", "reaction", "title", "description", "photo", "transaction_date", "transaction_url", "bot_payload", "msg_id", "extended_media", "subscription_period", "giveaway_post_id"]

    ID = 0xee7522d5
    QUALNAME = "types.StarsTransaction"

    def __init__(self, *, id: str, stars: int, date: int, peer: "raw.base.StarsTransactionPeer", refund: Optional[bool] = None, pending: Optional[bool] = None, failed: Optional[bool] = None, gift: Optional[bool] = None, reaction: Optional[bool] = None, title: Optional[str] = None, description: Optional[str] = None, photo: "raw.base.WebDocument" = None, transaction_date: Optional[int] = None, transaction_url: Optional[str] = None, bot_payload: Optional[bytes] = None, msg_id: Optional[int] = None, extended_media: Optional[List["raw.base.MessageMedia"]] = None, subscription_period: Optional[int] = None, giveaway_post_id: Optional[int] = None) -> None:
        self.id = id  # string
        self.stars = stars  # long
        self.date = date  # int
        self.peer = peer  # StarsTransactionPeer
        self.refund = refund  # flags.3?true
        self.pending = pending  # flags.4?true
        self.failed = failed  # flags.6?true
        self.gift = gift  # flags.10?true
        self.reaction = reaction  # flags.11?true
        self.title = title  # flags.0?string
        self.description = description  # flags.1?string
        self.photo = photo  # flags.2?WebDocument
        self.transaction_date = transaction_date  # flags.5?int
        self.transaction_url = transaction_url  # flags.5?string
        self.bot_payload = bot_payload  # flags.7?bytes
        self.msg_id = msg_id  # flags.8?int
        self.extended_media = extended_media  # flags.9?Vector<MessageMedia>
        self.subscription_period = subscription_period  # flags.12?int
        self.giveaway_post_id = giveaway_post_id  # flags.13?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarsTransaction":
        
        flags = Int.read(b)
        
        refund = True if flags & (1 << 3) else False
        pending = True if flags & (1 << 4) else False
        failed = True if flags & (1 << 6) else False
        gift = True if flags & (1 << 10) else False
        reaction = True if flags & (1 << 11) else False
        id = String.read(b)
        
        stars = Long.read(b)
        
        date = Int.read(b)
        
        peer = TLObject.read(b)
        
        title = String.read(b) if flags & (1 << 0) else None
        description = String.read(b) if flags & (1 << 1) else None
        photo = TLObject.read(b) if flags & (1 << 2) else None
        
        transaction_date = Int.read(b) if flags & (1 << 5) else None
        transaction_url = String.read(b) if flags & (1 << 5) else None
        bot_payload = Bytes.read(b) if flags & (1 << 7) else None
        msg_id = Int.read(b) if flags & (1 << 8) else None
        extended_media = TLObject.read(b) if flags & (1 << 9) else []
        
        subscription_period = Int.read(b) if flags & (1 << 12) else None
        giveaway_post_id = Int.read(b) if flags & (1 << 13) else None
        return StarsTransaction(id=id, stars=stars, date=date, peer=peer, refund=refund, pending=pending, failed=failed, gift=gift, reaction=reaction, title=title, description=description, photo=photo, transaction_date=transaction_date, transaction_url=transaction_url, bot_payload=bot_payload, msg_id=msg_id, extended_media=extended_media, subscription_period=subscription_period, giveaway_post_id=giveaway_post_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 3) if self.refund else 0
        flags |= (1 << 4) if self.pending else 0
        flags |= (1 << 6) if self.failed else 0
        flags |= (1 << 10) if self.gift else 0
        flags |= (1 << 11) if self.reaction else 0
        flags |= (1 << 0) if self.title is not None else 0
        flags |= (1 << 1) if self.description is not None else 0
        flags |= (1 << 2) if self.photo is not None else 0
        flags |= (1 << 5) if self.transaction_date is not None else 0
        flags |= (1 << 5) if self.transaction_url is not None else 0
        flags |= (1 << 7) if self.bot_payload is not None else 0
        flags |= (1 << 8) if self.msg_id is not None else 0
        flags |= (1 << 9) if self.extended_media else 0
        flags |= (1 << 12) if self.subscription_period is not None else 0
        flags |= (1 << 13) if self.giveaway_post_id is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.id))
        
        b.write(Long(self.stars))
        
        b.write(Int(self.date))
        
        b.write(self.peer.write())
        
        if self.title is not None:
            b.write(String(self.title))
        
        if self.description is not None:
            b.write(String(self.description))
        
        if self.photo is not None:
            b.write(self.photo.write())
        
        if self.transaction_date is not None:
            b.write(Int(self.transaction_date))
        
        if self.transaction_url is not None:
            b.write(String(self.transaction_url))
        
        if self.bot_payload is not None:
            b.write(Bytes(self.bot_payload))
        
        if self.msg_id is not None:
            b.write(Int(self.msg_id))
        
        if self.extended_media is not None:
            b.write(Vector(self.extended_media))
        
        if self.subscription_period is not None:
            b.write(Int(self.subscription_period))
        
        if self.giveaway_post_id is not None:
            b.write(Int(self.giveaway_post_id))
        
        return b.getvalue()
