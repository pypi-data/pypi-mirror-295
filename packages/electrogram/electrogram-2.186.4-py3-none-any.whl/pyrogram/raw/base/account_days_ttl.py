# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AccountDaysTTL = Union["raw.types.AccountDaysTTL"]


class AccountDaysTTL:  # type: ignore
    """Time-to-live of current account

    Constructors:
        This base type has 1 constructor available.

        .. currentmodule:: pyrogram.raw.types

        .. autosummary::
            :nosignatures:

            AccountDaysTTL

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetAccountTTL
    """

    QUALNAME = "pyrogram.raw.base.AccountDaysTTL"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
