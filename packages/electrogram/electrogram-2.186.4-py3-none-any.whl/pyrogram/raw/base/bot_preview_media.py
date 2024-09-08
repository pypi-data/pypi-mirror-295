# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BotPreviewMedia = Union["raw.types.BotPreviewMedia"]


class BotPreviewMedia:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 1 constructor available.

        .. currentmodule:: pyrogram.raw.types

        .. autosummary::
            :nosignatures:

            BotPreviewMedia

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            bots.AddPreviewMedia
            bots.EditPreviewMedia
            bots.GetPreviewMedias
    """

    QUALNAME = "pyrogram.raw.base.BotPreviewMedia"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
