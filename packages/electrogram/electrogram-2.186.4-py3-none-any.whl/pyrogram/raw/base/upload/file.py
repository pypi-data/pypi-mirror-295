# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

File = Union["raw.types.upload.File", "raw.types.upload.FileCdnRedirect"]


class File:  # type: ignore
    """Contains info on file.

    Constructors:
        This base type has 2 constructors available.

        .. currentmodule:: pyrogram.raw.types

        .. autosummary::
            :nosignatures:

            upload.File
            upload.FileCdnRedirect

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            upload.GetFile
    """

    QUALNAME = "pyrogram.raw.base.upload.File"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
