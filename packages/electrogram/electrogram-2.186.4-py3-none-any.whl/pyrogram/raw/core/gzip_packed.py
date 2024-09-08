from __future__ import annotations

from gzip import compress, decompress
from io import BytesIO
from typing import Any, cast

from .primitives.bytes import Bytes
from .primitives.int import Int
from .tl_object import TLObject


class GzipPacked(TLObject):
    ID = 0x3072CFA1

    __slots__ = ["packed_data"]

    QUALNAME = "GzipPacked"

    def __init__(self, packed_data: TLObject) -> None:
        self.packed_data = packed_data

    @staticmethod
    def read(data: BytesIO, *args: Any) -> GzipPacked:  # noqa: ARG004
        # Return the Object itself instead of a GzipPacked wrapping it
        return cast(GzipPacked, TLObject.read(BytesIO(decompress(Bytes.read(data)))))

    def write(self, *args: Any) -> bytes:  # noqa: ARG002
        b = BytesIO()

        b.write(Int(self.ID, False))

        b.write(Bytes(compress(self.packed_data.write())))

        return b.getvalue()
