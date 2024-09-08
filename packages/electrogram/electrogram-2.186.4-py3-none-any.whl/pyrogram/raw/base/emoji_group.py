# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmojiGroup = Union["raw.types.EmojiGroup", "raw.types.EmojiGroupGreeting", "raw.types.EmojiGroupPremium"]


class EmojiGroup:  # type: ignore
    """Represents an emoji category.

    Constructors:
        This base type has 3 constructors available.

        .. currentmodule:: pyrogram.raw.types

        .. autosummary::
            :nosignatures:

            EmojiGroup
            EmojiGroupGreeting
            EmojiGroupPremium
    """

    QUALNAME = "pyrogram.raw.base.EmojiGroup"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
