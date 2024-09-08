# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessageReactionsList = Union["raw.types.messages.MessageReactionsList"]


class MessageReactionsList:  # type: ignore
    """List of peers that reacted to a specific message

    Constructors:
        This base type has 1 constructor available.

        .. currentmodule:: pyrogram.raw.types

        .. autosummary::
            :nosignatures:

            messages.MessageReactionsList

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetMessageReactionsList
    """

    QUALNAME = "pyrogram.raw.base.messages.MessageReactionsList"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
