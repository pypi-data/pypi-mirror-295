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


class StarsRevenueStats(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.payments.StarsRevenueStats`.

    Details:
        - Layer: ``187``
        - ID: ``C92BB73B``

    Parameters:
        revenue_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        status (:obj:`StarsRevenueStatus <pyrogram.raw.base.StarsRevenueStatus>`):
            N/A

        usd_rate (``float`` ``64-bit``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetStarsRevenueStats
    """

    __slots__: List[str] = ["revenue_graph", "status", "usd_rate"]

    ID = 0xc92bb73b
    QUALNAME = "types.payments.StarsRevenueStats"

    def __init__(self, *, revenue_graph: "raw.base.StatsGraph", status: "raw.base.StarsRevenueStatus", usd_rate: float) -> None:
        self.revenue_graph = revenue_graph  # StatsGraph
        self.status = status  # StarsRevenueStatus
        self.usd_rate = usd_rate  # double

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarsRevenueStats":
        # No flags
        
        revenue_graph = TLObject.read(b)
        
        status = TLObject.read(b)
        
        usd_rate = Double.read(b)
        
        return StarsRevenueStats(revenue_graph=revenue_graph, status=status, usd_rate=usd_rate)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.revenue_graph.write())
        
        b.write(self.status.write())
        
        b.write(Double(self.usd_rate))
        
        return b.getvalue()
