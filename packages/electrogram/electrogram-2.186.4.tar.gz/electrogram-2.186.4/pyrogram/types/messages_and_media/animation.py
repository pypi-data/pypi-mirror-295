from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.file_id import (
    FileId,
    FileType,
    FileUniqueId,
    FileUniqueType,
    ThumbnailSource,
)
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class Animation(Object):
    """An animation file (GIF or H.264/MPEG-4 AVC video without sound).

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

        width (``int``):
            Animation width as defined by sender.

        height (``int``):
            Animation height as defined by sender.

        duration (``int``, *optional*):
            Duration of the animation in seconds as defined by sender.

        file_name (``str``, *optional*):
            Animation file name.

        mime_type (``str``, *optional*):
            Mime type of a file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the animation was sent.

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Animation thumbnails.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        file_id: str,
        file_unique_id: str,
        width: int,
        height: int,
        duration: int | None = None,
        file_name: str | None = None,
        mime_type: str | None = None,
        file_size: int | None = None,
        date: datetime | None = None,
        thumbs: list[types.Thumbnail] | None = None,
    ) -> None:
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.width = width
        self.height = height
        self.duration = duration
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client,
        animation: raw.types.Document,
        video_attributes: raw.types.DocumentAttributeVideo,
        file_name: str,
    ) -> Animation:
        return Animation(
            file_id=FileId(
                file_type=FileType.ANIMATION,
                dc_id=animation.dc_id,
                media_id=animation.id,
                access_hash=animation.access_hash,
                file_reference=animation.file_reference,
            ).encode(),
            file_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=animation.id,
            ).encode(),
            width=getattr(video_attributes, "w", 0),
            height=getattr(video_attributes, "h", 0),
            duration=getattr(video_attributes, "duration", 0),
            mime_type=animation.mime_type,
            file_size=animation.size,
            file_name=file_name,
            date=utils.timestamp_to_datetime(animation.date),
            thumbs=types.Thumbnail._parse(client, animation),
            client=client,
        )

    @staticmethod
    def _parse_chat_animation(client, video: raw.types.Photo) -> Animation:
        if isinstance(video, raw.types.Photo):
            if not video.video_sizes:
                return None
            video_sizes: list[raw.types.VideoSize] = [
                p for p in video.video_sizes if isinstance(p, raw.types.VideoSize)
            ]
            video_sizes.sort(key=lambda p: p.size)
            video_size = video_sizes[-1]
            return Animation(
                file_id=FileId(
                    file_type=FileType.PHOTO,
                    dc_id=video.dc_id,
                    media_id=video.id,
                    access_hash=video.access_hash,
                    file_reference=video.file_reference,
                    thumbnail_source=ThumbnailSource.THUMBNAIL,
                    thumbnail_file_type=FileType.PHOTO,
                    thumbnail_size=video_size.type,
                    volume_id=0,
                    local_id=0,
                ).encode()
                if video
                else None,
                file_unique_id=FileUniqueId(
                    file_unique_type=FileUniqueType.DOCUMENT,
                    media_id=video.id,
                ).encode()
                if video
                else None,
                width=video_size.w,
                height=video_size.h,
                file_size=video_size.size,
                date=utils.timestamp_to_datetime(video.date) if video else None,
                file_name=f"chat_video_{video.date}_{client.rnd_id()}.mp4",
                mime_type="video/mp4",
                client=client,
            )
        return None
