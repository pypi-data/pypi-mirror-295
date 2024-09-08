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


class PhoneConnectionWebrtc(TLObject):  # type: ignore
    """WebRTC connection parameters

    Constructor of :obj:`~pyrogram.raw.base.PhoneConnection`.

    Details:
        - Layer: ``187``
        - ID: ``635FE375``

    Parameters:
        id (``int`` ``64-bit``):
            Endpoint ID

        ip (``str``):
            IP address

        ipv6 (``str``):
            IPv6 address

        port (``int`` ``32-bit``):
            Port

        username (``str``):
            Username

        password (``str``):
            Password

        turn (``bool``, *optional*):
            Whether this is a TURN endpoint

        stun (``bool``, *optional*):
            Whether this is a STUN endpoint

    """

    __slots__: List[str] = ["id", "ip", "ipv6", "port", "username", "password", "turn", "stun"]

    ID = 0x635fe375
    QUALNAME = "types.PhoneConnectionWebrtc"

    def __init__(self, *, id: int, ip: str, ipv6: str, port: int, username: str, password: str, turn: Optional[bool] = None, stun: Optional[bool] = None) -> None:
        self.id = id  # long
        self.ip = ip  # string
        self.ipv6 = ipv6  # string
        self.port = port  # int
        self.username = username  # string
        self.password = password  # string
        self.turn = turn  # flags.0?true
        self.stun = stun  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PhoneConnectionWebrtc":
        
        flags = Int.read(b)
        
        turn = True if flags & (1 << 0) else False
        stun = True if flags & (1 << 1) else False
        id = Long.read(b)
        
        ip = String.read(b)
        
        ipv6 = String.read(b)
        
        port = Int.read(b)
        
        username = String.read(b)
        
        password = String.read(b)
        
        return PhoneConnectionWebrtc(id=id, ip=ip, ipv6=ipv6, port=port, username=username, password=password, turn=turn, stun=stun)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.turn else 0
        flags |= (1 << 1) if self.stun else 0
        b.write(Int(flags))
        
        b.write(Long(self.id))
        
        b.write(String(self.ip))
        
        b.write(String(self.ipv6))
        
        b.write(Int(self.port))
        
        b.write(String(self.username))
        
        b.write(String(self.password))
        
        return b.getvalue()
