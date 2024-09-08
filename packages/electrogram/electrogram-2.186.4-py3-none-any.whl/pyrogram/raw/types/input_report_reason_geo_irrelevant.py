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


class InputReportReasonGeoIrrelevant(TLObject):  # type: ignore
    """Report an irrelevant geogroup

    Constructor of :obj:`~pyrogram.raw.base.ReportReason`.

    Details:
        - Layer: ``187``
        - ID: ``DBD4FEED``

    Parameters:
        No parameters required.

    """

    __slots__: List[str] = []

    ID = 0xdbd4feed
    QUALNAME = "types.InputReportReasonGeoIrrelevant"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputReportReasonGeoIrrelevant":
        # No flags
        
        return InputReportReasonGeoIrrelevant()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
