from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING

from pymediainfo import MediaInfo

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.file_id import FileType

if TYPE_CHECKING:
    from datetime import datetime

log = logging.getLogger(__name__)


class SendMediaGroup:
    # TODO: Add progress parameter
    async def send_media_group(
        self: pyrogram.Client,
        chat_id: int | str,
        media: list[
            types.InputMediaPhoto
            | types.InputMediaVideo
            | types.InputMediaAudio
            | types.InputMediaDocument
            | types.InputMediaAnimation
        ],
        disable_notification: bool | None = None,
        message_thread_id: int | None = None,
        business_connection_id: str | None = None,
        reply_to_message_id: int | None = None,
        reply_to_story_id: int | None = None,
        reply_to_chat_id: int | str | None = None,
        quote_text: str | None = None,
        quote_entities: list[types.MessageEntity] | None = None,
        parse_mode: enums.ParseMode | None = None,
        schedule_date: datetime | None = None,
        protect_content: bool | None = None,
        message_effect_id: int | None = None,
        invert_media: bool | None = None,
    ) -> list[types.Message]:
        """Send a group of photos or videos as an album.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            media (List of :obj:`~pyrogram.types.InputMediaPhoto`, :obj:`~pyrogram.types.InputMediaVideo`, :obj:`~pyrogram.types.InputMediaAudio`, :obj:`~pyrogram.types.InputMediaDocument` and :obj:`~pyrogram.types.InputMediaAnimation`):
                A list describing photos and videos to be sent, must include 2–10 items.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.
                for forum supergroups only.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_to_story_id (``int``, *optional*):
                Unique identifier for the target story.

            reply_to_chat_id (``int`` | ``str``, *optional*):
                Unique identifier for the origin chat.
                for reply to message from another chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, quote_text are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.
                For quote_text.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            invert_media (``bool``, *optional*):
                Inverts the position of the media and caption.

        Returns:
            List of :obj:`~pyrogram.types.Message`: On success, a list of the sent messages is returned.

        Example:
            .. code-block:: python

                from pyrogram.types import InputMediaPhoto, InputMediaVideo

                await app.send_media_group(
                    "me",
                    [
                        InputMediaPhoto("photo1.jpg"),
                        InputMediaPhoto("photo2.jpg", caption="photo caption"),
                        InputMediaVideo("video.mp4", caption="video caption")
                    ]
                )
        """
        multi_media = []

        reply_to = await utils.get_reply_to(
            client=self,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_story_id=reply_to_story_id,
            message_thread_id=message_thread_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            parse_mode=parse_mode,
        )

        for i in media:
            if isinstance(i, types.InputMediaPhoto):
                if isinstance(i.media, str):
                    if Path(i.media).is_file():
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedPhoto(
                                    file=await self.save_file(i.media),
                                    spoiler=i.has_spoiler,
                                ),
                            )
                        )

                        media = raw.types.InputMediaPhoto(
                            id=raw.types.InputPhoto(
                                id=media.photo.id,
                                access_hash=media.photo.access_hash,
                                file_reference=media.photo.file_reference,
                            ),
                            spoiler=i.has_spoiler,
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaPhotoExternal(
                                    url=i.media, spoiler=i.has_spoiler
                                ),
                            )
                        )

                        media = raw.types.InputMediaPhoto(
                            id=raw.types.InputPhoto(
                                id=media.photo.id,
                                access_hash=media.photo.access_hash,
                                file_reference=media.photo.file_reference,
                            ),
                            spoiler=i.has_spoiler,
                        )
                    else:
                        media = utils.get_input_media_from_file_id(
                            i.media, FileType.PHOTO
                        )
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedPhoto(
                                file=await self.save_file(i.media),
                                spoiler=i.has_spoiler,
                            ),
                        )
                    )

                    media = raw.types.InputMediaPhoto(
                        id=raw.types.InputPhoto(
                            id=media.photo.id,
                            access_hash=media.photo.access_hash,
                            file_reference=media.photo.file_reference,
                        ),
                        spoiler=i.has_spoiler,
                    )
            elif isinstance(i, types.InputMediaVideo | types.InputMediaAnimation):
                if isinstance(i.media, str):
                    is_animation = False
                    if Path(i.media).is_file():
                        try:
                            videoInfo = MediaInfo.parse(i.media)
                        except OSError:
                            is_animation = bool(
                                isinstance(i, types.InputMediaAnimation)
                            )
                        else:
                            if not any(
                                track.track_type == "Audio"
                                for track in videoInfo.tracks
                            ):
                                is_animation = True
                        attributes = [
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=True
                                if is_animation
                                else (i.supports_streaming or None),
                                duration=i.duration,
                                w=i.width,
                                h=i.height,
                            ),
                            raw.types.DocumentAttributeFilename(
                                file_name=Path(i.media).name
                            ),
                        ]
                        if is_animation:
                            attributes.append(raw.types.DocumentAttributeAnimated())
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedDocument(
                                    file=await self.save_file(i.media),
                                    thumb=await self.save_file(i.thumb),
                                    spoiler=i.has_spoiler,
                                    mime_type=self.guess_mime_type(i.media)
                                    or "video/mp4",
                                    nosound_video=is_animation,
                                    attributes=attributes,
                                ),
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            ),
                            spoiler=i.has_spoiler,
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaDocumentExternal(
                                    url=i.media, spoiler=i.has_spoiler
                                ),
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            ),
                            spoiler=i.has_spoiler,
                        )
                    else:
                        media = utils.get_input_media_from_file_id(
                            i.media, FileType.VIDEO
                        )
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedDocument(
                                file=await self.save_file(i.media),
                                thumb=await self.save_file(i.thumb),
                                spoiler=i.has_spoiler,
                                mime_type=self.guess_mime_type(
                                    getattr(i.media, "name", "video.mp4")
                                )
                                or "video/mp4",
                                attributes=[
                                    raw.types.DocumentAttributeVideo(
                                        supports_streaming=i.supports_streaming
                                        or None,
                                        duration=i.duration,
                                        w=i.width,
                                        h=i.height,
                                    ),
                                    raw.types.DocumentAttributeFilename(
                                        file_name=getattr(
                                            i.media,
                                            "name",
                                            "video.mp4",
                                        )
                                    ),
                                ],
                            ),
                        )
                    )

                    media = raw.types.InputMediaDocument(
                        id=raw.types.InputDocument(
                            id=media.document.id,
                            access_hash=media.document.access_hash,
                            file_reference=media.document.file_reference,
                        ),
                        spoiler=i.has_spoiler,
                    )
            elif isinstance(i, types.InputMediaAudio):
                if isinstance(i.media, str):
                    if Path(i.media).is_file():
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedDocument(
                                    mime_type=self.guess_mime_type(i.media)
                                    or "audio/mpeg",
                                    file=await self.save_file(i.media),
                                    thumb=await self.save_file(i.thumb),
                                    attributes=[
                                        raw.types.DocumentAttributeAudio(
                                            duration=i.duration,
                                            performer=i.performer,
                                            title=i.title,
                                        ),
                                        raw.types.DocumentAttributeFilename(
                                            file_name=Path(i.media).name
                                        ),
                                    ],
                                ),
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            )
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaDocumentExternal(
                                    url=i.media
                                ),
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            )
                        )
                    else:
                        media = utils.get_input_media_from_file_id(
                            i.media, FileType.AUDIO
                        )
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedDocument(
                                mime_type=self.guess_mime_type(
                                    getattr(i.media, "name", "audio.mp3")
                                )
                                or "audio/mpeg",
                                file=await self.save_file(i.media),
                                thumb=await self.save_file(i.thumb),
                                attributes=[
                                    raw.types.DocumentAttributeAudio(
                                        duration=i.duration,
                                        performer=i.performer,
                                        title=i.title,
                                    ),
                                    raw.types.DocumentAttributeFilename(
                                        file_name=getattr(
                                            i.media,
                                            "name",
                                            "audio.mp3",
                                        )
                                    ),
                                ],
                            ),
                        )
                    )

                    media = raw.types.InputMediaDocument(
                        id=raw.types.InputDocument(
                            id=media.document.id,
                            access_hash=media.document.access_hash,
                            file_reference=media.document.file_reference,
                        )
                    )
            elif isinstance(i, types.InputMediaDocument):
                if isinstance(i.media, str):
                    if Path(i.media).is_file():
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedDocument(
                                    mime_type=self.guess_mime_type(i.media)
                                    or "application/zip",
                                    file=await self.save_file(i.media),
                                    thumb=await self.save_file(i.thumb),
                                    attributes=[
                                        raw.types.DocumentAttributeFilename(
                                            file_name=Path(i.media).name
                                        )
                                    ],
                                ),
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            )
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaDocumentExternal(
                                    url=i.media
                                ),
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            )
                        )
                    else:
                        media = utils.get_input_media_from_file_id(
                            i.media, FileType.DOCUMENT
                        )
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedDocument(
                                mime_type=self.guess_mime_type(
                                    getattr(i.media, "name", "file.zip")
                                )
                                or "application/zip",
                                file=await self.save_file(i.media),
                                thumb=await self.save_file(i.thumb),
                                attributes=[
                                    raw.types.DocumentAttributeFilename(
                                        file_name=getattr(
                                            i.media,
                                            "name",
                                            "file.zip",
                                        )
                                    )
                                ],
                            ),
                        )
                    )

                    media = raw.types.InputMediaDocument(
                        id=raw.types.InputDocument(
                            id=media.document.id,
                            access_hash=media.document.access_hash,
                            file_reference=media.document.file_reference,
                        )
                    )
            else:
                raise ValueError(
                    f"{i.__class__.__name__} is not a supported type for send_media_group"
                )

            multi_media.append(
                raw.types.InputSingleMedia(
                    media=media,
                    random_id=self.rnd_id(),
                    **await self.parser.parse(i.caption, i.parse_mode),
                )
            )

        rpc = raw.functions.messages.SendMultiMedia(
            peer=await self.resolve_peer(chat_id),
            multi_media=multi_media,
            silent=disable_notification or None,
            reply_to=reply_to,
            schedule_date=utils.datetime_to_timestamp(schedule_date),
            noforwards=protect_content,
            effect=message_effect_id,
            invert_media=invert_media,
        )

        if business_connection_id is not None:
            r = await self.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    connection_id=business_connection_id, query=rpc
                ),
                sleep_threshold=60,
            )
        else:
            r = await self.invoke(rpc, sleep_threshold=60)

        return await utils.parse_messages(
            self,
            raw.types.messages.Messages(
                messages=[
                    m.message
                    for m in filter(
                        lambda u: isinstance(
                            u,
                            raw.types.UpdateNewMessage
                            | raw.types.UpdateNewChannelMessage
                            | raw.types.UpdateNewScheduledMessage
                            | raw.types.UpdateBotNewBusinessMessage,
                        ),
                        r.updates,
                    )
                ],
                users=r.users,
                chats=r.chats,
            ),
            business_connection_id=business_connection_id,
        )
