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


class InputThemeSettings(TLObject):  # type: ignore
    """Theme settings

    Constructor of :obj:`~pyrogram.raw.base.InputThemeSettings`.

    Details:
        - Layer: ``187``
        - ID: ``8FDE504F``

    Parameters:
        base_theme (:obj:`BaseTheme <pyrogram.raw.base.BaseTheme>`):
            Default theme on which this theme is based

        accent_color (``int`` ``32-bit``):
            Accent color, ARGB format

        message_colors_animated (``bool``, *optional*):
            If set, the freeform gradient fill needs to be animated on every sent message

        outbox_accent_color (``int`` ``32-bit``, *optional*):
            Accent color of outgoing messages in ARGB format

        message_colors (List of ``int`` ``32-bit``, *optional*):
            The fill to be used as a background for outgoing messages, in RGB24 format. If just one or two equal colors are provided, describes a solid fill of a background. If two different colors are provided, describes the top and bottom colors of a 0-degree gradient.If three or four colors are provided, describes a freeform gradient fill of a background.

        wallpaper (:obj:`InputWallPaper <pyrogram.raw.base.InputWallPaper>`, *optional*):
            inputWallPaper or inputWallPaperSlug when passing wallpaper files for image or pattern wallpapers, inputWallPaperNoFile with id=0 otherwise.

        wallpaper_settings (:obj:`WallPaperSettings <pyrogram.raw.base.WallPaperSettings>`, *optional*):
            Wallpaper settings.

    """

    __slots__: List[str] = ["base_theme", "accent_color", "message_colors_animated", "outbox_accent_color", "message_colors", "wallpaper", "wallpaper_settings"]

    ID = 0x8fde504f
    QUALNAME = "types.InputThemeSettings"

    def __init__(self, *, base_theme: "raw.base.BaseTheme", accent_color: int, message_colors_animated: Optional[bool] = None, outbox_accent_color: Optional[int] = None, message_colors: Optional[List[int]] = None, wallpaper: "raw.base.InputWallPaper" = None, wallpaper_settings: "raw.base.WallPaperSettings" = None) -> None:
        self.base_theme = base_theme  # BaseTheme
        self.accent_color = accent_color  # int
        self.message_colors_animated = message_colors_animated  # flags.2?true
        self.outbox_accent_color = outbox_accent_color  # flags.3?int
        self.message_colors = message_colors  # flags.0?Vector<int>
        self.wallpaper = wallpaper  # flags.1?InputWallPaper
        self.wallpaper_settings = wallpaper_settings  # flags.1?WallPaperSettings

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputThemeSettings":
        
        flags = Int.read(b)
        
        message_colors_animated = True if flags & (1 << 2) else False
        base_theme = TLObject.read(b)
        
        accent_color = Int.read(b)
        
        outbox_accent_color = Int.read(b) if flags & (1 << 3) else None
        message_colors = TLObject.read(b, Int) if flags & (1 << 0) else []
        
        wallpaper = TLObject.read(b) if flags & (1 << 1) else None
        
        wallpaper_settings = TLObject.read(b) if flags & (1 << 1) else None
        
        return InputThemeSettings(base_theme=base_theme, accent_color=accent_color, message_colors_animated=message_colors_animated, outbox_accent_color=outbox_accent_color, message_colors=message_colors, wallpaper=wallpaper, wallpaper_settings=wallpaper_settings)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.message_colors_animated else 0
        flags |= (1 << 3) if self.outbox_accent_color is not None else 0
        flags |= (1 << 0) if self.message_colors else 0
        flags |= (1 << 1) if self.wallpaper is not None else 0
        flags |= (1 << 1) if self.wallpaper_settings is not None else 0
        b.write(Int(flags))
        
        b.write(self.base_theme.write())
        
        b.write(Int(self.accent_color))
        
        if self.outbox_accent_color is not None:
            b.write(Int(self.outbox_accent_color))
        
        if self.message_colors is not None:
            b.write(Vector(self.message_colors, Int))
        
        if self.wallpaper is not None:
            b.write(self.wallpaper.write())
        
        if self.wallpaper_settings is not None:
            b.write(self.wallpaper_settings.write())
        
        return b.getvalue()
