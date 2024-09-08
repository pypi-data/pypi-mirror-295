count = 604

exceptions = {
    401: {
        "_": "Unauthorized",
        "ACTIVE_USER_REQUIRED": "ActiveUserRequired",
        "AUTH_KEY_INVALID": "AuthKeyInvalid",
        "AUTH_KEY_PERM_EMPTY": "AuthKeyPermEmpty",
        "AUTH_KEY_UNREGISTERED": "AuthKeyUnregistered",
        "SESSION_EXPIRED": "SessionExpired",
        "SESSION_PASSWORD_NEEDED": "SessionPasswordNeeded",
        "SESSION_REVOKED": "SessionRevoked",
        "USER_DEACTIVATED": "UserDeactivated",
        "USER_DEACTIVATED_BAN": "UserDeactivatedBan",
    },
    500: {
        "_": "InternalServerError",
        "API_CALL_ERROR": "ApiCallError",
        "AUTH_RESTART": "AuthRestart",
        "CALL_OCCUPY_FAILED": "CallOccupyFailed",
        "CHAT_ID_GENERATE_FAILED": "ChatIdGenerateFailed",
        "CHAT_OCCUPY_LOC_FAILED": "ChatOccupyLocFailed",
        "CHAT_OCCUPY_USERNAME_FAILED": "ChatOccupyUsernameFailed",
        "CHP_CALL_FAIL": "ChpCallFail",
        "ENCRYPTION_OCCUPY_ADMIN_FAILED": "EncryptionOccupyAdminFailed",
        "ENCRYPTION_OCCUPY_FAILED": "EncryptionOccupyFailed",
        "FOLDER_DEAC_AUTOFIX_ALL": "FolderDeacAutofixAll",
        "GROUPCALL_ADD_PARTICIPANTS_FAILED": "GroupcallAddParticipantsFailed",
        "GROUPED_ID_OCCUPY_FAILED": "GroupedIdOccupyFailed",
        "HISTORY_GET_FAILED": "HistoryGetFailed",
        "IMAGE_ENGINE_DOWN": "ImageEngineDown",
        "INTERDC_X_CALL_ERROR": "InterdcCallError",
        "INTERDC_X_CALL_RICH_ERROR": "InterdcCallRichError",
        "MEMBER_FETCH_FAILED": "MemberFetchFailed",
        "MEMBER_NO_LOCATION": "MemberNoLocation",
        "MEMBER_OCCUPY_PRIMARY_LOC_FAILED": "MemberOccupyPrimaryLocFailed",
        "MEMBER_OCCUPY_USERNAME_FAILED": "MemberOccupyUsernameFailed",
        "MSGID_DECREASE_RETRY": "MsgidDecreaseRetry",
        "MSG_RANGE_UNSYNC": "MsgRangeUnsync",
        "MT_SEND_QUEUE_TOO_LONG": "MtSendQueueTooLong",
        "NEED_CHAT_INVALID": "NeedChatInvalid",
        "NEED_MEMBER_INVALID": "NeedMemberInvalid",
        "No workers running": "NoWorkersRunning",
        "PARTICIPANT_CALL_FAILED": "ParticipantCallFailed",
        "PERSISTENT_TIMESTAMP_OUTDATED": "PersistentTimestampOutdated",
        "PHOTO_CREATE_FAILED": "PhotoCreateFailed",
        "POSTPONED_TIMEOUT": "PostponedTimeout",
        "PTS_CHANGE_EMPTY": "PtsChangeEmpty",
        "RANDOM_ID_DUPLICATE": "RandomIdDuplicate",
        "REG_ID_GENERATE_FAILED": "RegIdGenerateFailed",
        "RPC_CALL_FAIL": "RpcCallFail",
        "RPC_CONNECT_FAILED": "RpcConnectFailed",
        "RPC_MCGET_FAIL": "RpcMcgetFail",
        "SIGN_IN_FAILED": "SignInFailed",
        "STORAGE_CHECK_FAILED": "StorageCheckFailed",
        "STORE_INVALID_SCALAR_TYPE": "StoreInvalidScalarType",
        "TIMEOUT": "Timeout",
        "UNKNOWN_METHOD": "UnknownMethod",
        "UPLOAD_NO_VOLUME": "UploadNoVolume",
        "VOLUME_LOC_NOT_FOUND": "VolumeLocNotFound",
        "WORKER_BUSY_TOO_LONG_RETRY": "WorkerBusyTooLongRetry",
        "WP_ID_GENERATE_FAILED": "WpIdGenerateFailed",
        "FILE_WRITE_FAILED": "FileWriteFailed",
        "CHAT_FROM_CALL_CHANGED": "ChatFromCallChanged",
    },
    403: {
        "_": "Forbidden",
        "BROADCAST_FORBIDDEN": "BroadcastForbidden",
        "CHANNEL_PUBLIC_GROUP_NA": "ChannelPublicGroupNa",
        "CHAT_ADMIN_INVITE_REQUIRED": "ChatAdminInviteRequired",
        "CHAT_ADMIN_REQUIRED": "ChatAdminRequired",
        "CHAT_FORBIDDEN": "ChatForbidden",
        "CHAT_GUEST_SEND_FORBIDDEN": "ChatGuestSendForbidden",
        "EDIT_BOT_INVITE_FORBIDDEN": "EditBotInviteForbidden",
        "INLINE_BOT_REQUIRED": "InlineBotRequired",
        "MESSAGE_AUTHOR_REQUIRED": "MessageAuthorRequired",
        "MESSAGE_DELETE_FORBIDDEN": "MessageDeleteForbidden",
        "NOT_ALLOWED": "NotAllowed",
        "NOT_ELIGIBLE": "NotEligible",
        "PARTICIPANT_JOIN_MISSING": "ParticipantJoinMissing",
        "POLL_VOTE_REQUIRED": "PollVoteRequired",
        "PREMIUM_ACCOUNT_REQUIRED": "PremiumAccountRequired",
        "PRIVACY_PREMIUM_REQUIRED": "PrivacyPremiumRequired",
        "PUBLIC_CHANNEL_MISSING": "PublicChannelMissing",
        "RIGHT_FORBIDDEN": "RightForbidden",
        "SENSITIVE_CHANGE_FORBIDDEN": "SensitiveChangeForbidden",
        "TAKEOUT_REQUIRED": "TakeoutRequired",
        "USER_BOT_INVALID": "UserBotInvalid",
        "USER_CHANNELS_TOO_MUCH": "UserChannelsTooMuch",
        "USER_DELETED": "UserDeleted",
        "USER_INVALID": "UserInvalid",
        "USER_IS_BLOCKED": "UserIsBlocked",
        "USER_NOT_MUTUAL_CONTACT": "UserNotMutualContact",
        "USER_PRIVACY_RESTRICTED": "UserPrivacyRestricted",
        "USER_RESTRICTED": "UserRestricted",
        "CHAT_SEND_AUDIOS_FORBIDDEN": "ChatSendAudiosForbidden",
        "CHAT_SEND_DOCS_FORBIDDEN": "ChatSendDocsForbidden",
        "CHAT_SEND_GAME_FORBIDDEN": "ChatSendGameForbidden",
        "CHAT_SEND_GIFS_FORBIDDEN": "ChatSendGifsForbidden",
        "CHAT_SEND_INLINE_FORBIDDEN": "ChatSendInlineForbidden",
        "CHAT_SEND_MEDIA_FORBIDDEN": "ChatSendMediaForbidden",
        "CHAT_SEND_PHOTOS_FORBIDDEN": "ChatSendPhotosForbidden",
        "CHAT_SEND_PLAIN_FORBIDDEN": "ChatSendPlainForbidden",
        "CHAT_SEND_POLL_FORBIDDEN": "ChatSendPollForbidden",
        "CHAT_SEND_STICKERS_FORBIDDEN": "ChatSendStickersForbidden",
        "CHAT_SEND_VIDEOS_FORBIDDEN": "ChatSendVideosForbidden",
        "CHAT_SEND_VOICES_FORBIDDEN": "ChatSendVoicesForbidden",
        "CHAT_WRITE_FORBIDDEN": "ChatWriteForbidden",
        "GROUPCALL_ALREADY_STARTED": "GroupcallAlreadyStarted",
        "GROUPCALL_FORBIDDEN": "GroupcallForbidden",
        "LIVE_DISABLED": "LiveDisabled",
        "CHAT_GUEST_SEND_FORBIDDEN": "ChatGuestSendForbidden",
    },
    406: {
        "_": "NotAcceptable",
        "AUTH_KEY_DUPLICATED": "AuthKeyDuplicated",
        "CHANNEL_PRIVATE": "ChannelPrivate",
        "CHANNEL_TOO_LARGE": "ChannelTooLarge",
        "CHAT_FORWARDS_RESTRICTED": "ChatForwardsRestricted",
        "FILEREF_UPGRADE_NEEDED": "FilerefUpgradeNeeded",
        "FRESH_CHANGE_ADMINS_FORBIDDEN": "FreshChangeAdminsForbidden",
        "FRESH_CHANGE_PHONE_FORBIDDEN": "FreshChangePhoneForbidden",
        "FRESH_RESET_AUTHORISATION_FORBIDDEN": "FreshResetAuthorisationForbidden",
        "GIFTCODE_NOT_ALLOWED": "GiftcodeNotAllowed",
        "INVITE_HASH_EXPIRED": "InviteHashExpired",
        "PHONE_NUMBER_INVALID": "PhoneNumberInvalid",
        "PHONE_PASSWORD_FLOOD": "PhonePasswordFlood",
        "PREMIUM_CURRENTLY_UNAVAILABLE": "PremiumCurrentlyUnavailable",
        "PREVIOUS_CHAT_IMPORT_ACTIVE_WAIT_XMIN": "PreviousChatImportActiveWaitMin",
        "SEND_CODE_UNAVAILABLE": "SendCodeUnavailable",
        "STICKERSET_INVALID": "StickersetInvalid",
        "STICKERSET_OWNER_ANONYMOUS": "StickersetOwnerAnonymous",
        "UPDATE_APP_TO_LOGIN": "UpdateAppToLogin",
        "USERPIC_PRIVACY_REQUIRED": "UserpicPrivacyRequired",
        "USERPIC_UPLOAD_REQUIRED": "UserpicUploadRequired",
        "USER_RESTRICTED": "UserRestricted",
    },
    303: {
        "_": "SeeOther",
        "FILE_MIGRATE_X": "FileMigrate",
        "NETWORK_MIGRATE_X": "NetworkMigrate",
        "PHONE_MIGRATE_X": "PhoneMigrate",
        "STATS_MIGRATE_X": "StatsMigrate",
        "USER_MIGRATE_X": "UserMigrate",
    },
    503: {
        "_": "ServiceUnavailable",
        "ApiCallError": "ApiCallError",
        "Timeout": "Timeout",
        "Timedout": "Timedout",
    },
    400: {
        "_": "BadRequest",
        "ABOUT_TOO_LONG": "AboutTooLong",
        "ACCESS_TOKEN_EXPIRED": "AccessTokenExpired",
        "ACCESS_TOKEN_INVALID": "AccessTokenInvalid",
        "ADMINS_TOO_MUCH": "AdminsTooMuch",
        "ADMIN_ID_INVALID": "AdminIdInvalid",
        "ADMIN_RANK_EMOJI_NOT_ALLOWED": "AdminRankEmojiNotAllowed",
        "ADMIN_RANK_INVALID": "AdminRankInvalid",
        "ALBUM_PHOTOS_TOO_MANY": "AlbumPhotosTooMany",
        "API_ID_INVALID": "ApiIdInvalid",
        "API_ID_PUBLISHED_FLOOD": "ApiIdPublishedFlood",
        "ARTICLE_TITLE_EMPTY": "ArticleTitleEmpty",
        "AUDIO_CONTENT_URL_EMPTY": "AudioContentUrlEmpty",
        "AUDIO_TITLE_EMPTY": "AudioTitleEmpty",
        "AUTH_BYTES_INVALID": "AuthBytesInvalid",
        "AUTH_TOKEN_ALREADY_ACCEPTED": "AuthTokenAlreadyAccepted",
        "AUTH_TOKEN_EXCEPTION": "AuthTokenException",
        "AUTH_TOKEN_EXPIRED": "AuthTokenExpired",
        "AUTH_TOKEN_INVALID": "AuthTokenInvalid",
        "AUTH_TOKEN_INVALID2": "AuthTokenInvalid2",
        "AUTH_TOKEN_INVALIDX": "AuthTokenInvalidx",
        "AUTOARCHIVE_NOT_AVAILABLE": "AutoarchiveNotAvailable",
        "BANK_CARD_NUMBER_INVALID": "BankCardNumberInvalid",
        "BANNED_RIGHTS_INVALID": "BannedRightsInvalid",
        "BASE_PORT_LOC_INVALID": "BasePortLocInvalid",
        "BOTS_TOO_MUCH": "BotsTooMuch",
        "BOT_CHANNELS_NA": "BotChannelsNa",
        "BOT_COMMAND_DESCRIPTION_INVALID": "BotCommandDescriptionInvalid",
        "BOT_COMMAND_INVALID": "BotCommandInvalid",
        "BOT_DOMAIN_INVALID": "BotDomainInvalid",
        "BOT_GAMES_DISABLED": "BotGamesDisabled",
        "BOT_GROUPS_BLOCKED": "BotGroupsBlocked",
        "BOT_INLINE_DISABLED": "BotInlineDisabled",
        "BOT_INVALID": "BotInvalid",
        "BOT_METHOD_INVALID": "BotMethodInvalid",
        "BOT_MISSING": "BotMissing",
        "BOT_ONESIDE_NOT_AVAIL": "BotOnesideNotAvail",
        "BOT_PAYMENTS_DISABLED": "BotPaymentsDisabled",
        "BOT_POLLS_DISABLED": "BotPollsDisabled",
        "BOT_RESPONSE_TIMEOUT": "BotResponseTimeout",
        "BOT_SCORE_NOT_MODIFIED": "BotScoreNotModified",
        "BROADCAST_CALLS_DISABLED": "BroadcastCallsDisabled",
        "BROADCAST_ID_INVALID": "BroadcastIdInvalid",
        "BROADCAST_PUBLIC_VOTERS_FORBIDDEN": "BroadcastPublicVotersForbidden",
        "BROADCAST_REQUIRED": "BroadcastRequired",
        "BUTTON_DATA_INVALID": "ButtonDataInvalid",
        "BUTTON_TEXT_INVALID": "ButtonTextInvalid",
        "BUTTON_TYPE_INVALID": "ButtonTypeInvalid",
        "BUTTON_URL_INVALID": "ButtonUrlInvalid",
        "BUTTON_USER_PRIVACY_RESTRICTED": "ButtonUserPrivacyRestricted",
        "CALL_ALREADY_ACCEPTED": "CallAlreadyAccepted",
        "CALL_ALREADY_DECLINED": "CallAlreadyDeclined",
        "CALL_PEER_INVALID": "CallPeerInvalid",
        "CALL_PROTOCOL_FLAGS_INVALID": "CallProtocolFlagsInvalid",
        "CDN_METHOD_INVALID": "CdnMethodInvalid",
        "CHANNELS_ADMIN_LOCATED_TOO_MUCH": "ChannelsAdminLocatedTooMuch",
        "CHANNELS_ADMIN_PUBLIC_TOO_MUCH": "ChannelsAdminPublicTooMuch",
        "CHANNELS_TOO_MUCH": "ChannelsTooMuch",
        "CHANNEL_ADD_INVALID": "ChannelAddInvalid",
        "CHANNEL_BANNED": "ChannelBanned",
        "CHANNEL_INVALID": "ChannelInvalid",
        "CHANNEL_PARICIPANT_MISSING": "ChannelParicipantMissing",
        "CHANNEL_PRIVATE": "ChannelPrivate",
        "CHANNEL_TOO_BIG": "ChannelTooBig",
        "CHANNEL_TOO_LARGE": "ChannelTooLarge",
        "CHARGE_ALREADY_REFUNDED": "ChargeAlreadyRefunded",
        "CHARGE_NOT_FOUND": "ChargeNotFound",
        "CHAT_ABOUT_NOT_MODIFIED": "ChatAboutNotModified",
        "CHAT_ABOUT_TOO_LONG": "ChatAboutTooLong",
        "CHAT_ADMIN_REQUIRED": "ChatAdminRequired",
        "CHAT_DISCUSSION_UNALLOWED": "ChatDiscussionUnallowed",
        "CHAT_FORWARDS_RESTRICTED": "ChatForwardsRestricted",
        "CHAT_ID_EMPTY": "ChatIdEmpty",
        "CHAT_ID_INVALID": "ChatIdInvalid",
        "CHAT_INVALID": "ChatInvalid",
        "CHAT_INVITE_PERMANENT": "ChatInvitePermanent",
        "CHAT_LINK_EXISTS": "ChatLinkExists",
        "CHAT_NOT_MODIFIED": "ChatNotModified",
        "CHAT_RESTRICTED": "ChatRestricted",
        "CHAT_REVOKE_DATE_UNSUPPORTED": "ChatRevokeDateUnsupported",
        "CHAT_SEND_INLINE_FORBIDDEN": "ChatSendInlineForbidden",
        "CHAT_TITLE_EMPTY": "ChatTitleEmpty",
        "CHAT_TOO_BIG": "ChatTooBig",
        "CODE_EMPTY": "CodeEmpty",
        "CODE_HASH_INVALID": "CodeHashInvalid",
        "CODE_INVALID": "CodeInvalid",
        "COLOR_INVALID": "ColorInvalid",
        "CONNECTION_API_ID_INVALID": "ConnectionApiIdInvalid",
        "CONNECTION_APP_VERSION_EMPTY": "ConnectionAppVersionEmpty",
        "CONNECTION_DEVICE_MODEL_EMPTY": "ConnectionDeviceModelEmpty",
        "CONNECTION_LANG_PACK_INVALID": "ConnectionLangPackInvalid",
        "CONNECTION_LAYER_INVALID": "ConnectionLayerInvalid",
        "CONNECTION_NOT_INITED": "ConnectionNotInited",
        "CONNECTION_SYSTEM_EMPTY": "ConnectionSystemEmpty",
        "CONNECTION_SYSTEM_LANG_CODE_EMPTY": "ConnectionSystemLangCodeEmpty",
        "CONTACT_ADD_MISSING": "ContactAddMissing",
        "CONTACT_ID_INVALID": "ContactIdInvalid",
        "CONTACT_NAME_EMPTY": "ContactNameEmpty",
        "CONTACT_REQ_MISSING": "ContactReqMissing",
        "CREATE_CALL_FAILED": "CreateCallFailed",
        "CURRENCY_TOTAL_AMOUNT_INVALID": "CurrencyTotalAmountInvalid",
        "DATA_INVALID": "DataInvalid",
        "DATA_JSON_INVALID": "DataJsonInvalid",
        "DATA_TOO_LONG": "DataTooLong",
        "DATE_EMPTY": "DateEmpty",
        "DC_ID_INVALID": "DcIdInvalid",
        "DH_G_A_INVALID": "DhGAInvalid",
        "DOCUMENT_INVALID": "DocumentInvalid",
        "EMAIL_HASH_EXPIRED": "EmailHashExpired",
        "EMAIL_INVALID": "EmailInvalid",
        "EMAIL_NOT_ALLOWED": "EmailNotAllowed",
        "EMAIL_UNCONFIRMED": "EmailUnconfirmed",
        "EMAIL_UNCONFIRMED_X": "EmailUnconfirmed",
        "EMAIL_VERIFY_EXPIRED": "EmailVerifyExpired",
        "EMOJI_INVALID": "EmojiInvalid",
        "EMOJI_NOT_MODIFIED": "EmojiNotModified",
        "EMOTICON_EMPTY": "EmoticonEmpty",
        "EMOTICON_INVALID": "EmoticonInvalid",
        "EMOTICON_STICKERPACK_MISSING": "EmoticonStickerpackMissing",
        "ENCRYPTED_MESSAGE_INVALID": "EncryptedMessageInvalid",
        "ENCRYPTION_ALREADY_ACCEPTED": "EncryptionAlreadyAccepted",
        "ENCRYPTION_ALREADY_DECLINED": "EncryptionAlreadyDeclined",
        "ENCRYPTION_DECLINED": "EncryptionDeclined",
        "ENCRYPTION_ID_INVALID": "EncryptionIdInvalid",
        "ENTITIES_TOO_LONG": "EntitiesTooLong",
        "ENTITY_BOUNDS_INVALID": "EntityBoundsInvalid",
        "ENTITY_MENTION_USER_INVALID": "EntityMentionUserInvalid",
        "ERROR_TEXT_EMPTY": "ErrorTextEmpty",
        "EXPIRE_DATE_INVALID": "ExpireDateInvalid",
        "EXPIRE_FORBIDDEN": "ExpireForbidden",
        "EXPORT_CARD_INVALID": "ExportCardInvalid",
        "EXTERNAL_URL_INVALID": "ExternalUrlInvalid",
        "FIELD_NAME_EMPTY": "FieldNameEmpty",
        "FIELD_NAME_INVALID": "FieldNameInvalid",
        "FILE_CONTENT_TYPE_INVALID": "FileContentTypeInvalid",
        "FILE_EMTPY": "FileEmtpy",
        "FILE_ID_INVALID": "FileIdInvalid",
        "FILE_MIGRATE_X": "FileMigrate",
        "FILE_PARTS_INVALID": "FilePartsInvalid",
        "FILE_PART_0_MISSING": "FilePart0Missing",
        "FILE_PART_EMPTY": "FilePartEmpty",
        "FILE_PART_INVALID": "FilePartInvalid",
        "FILE_PART_LENGTH_INVALID": "FilePartLengthInvalid",
        "FILE_PART_SIZE_CHANGED": "FilePartSizeChanged",
        "FILE_PART_SIZE_INVALID": "FilePartSizeInvalid",
        "FILE_PART_TOO_BIG": "FilePartTooBig",
        "FILE_PART_X_MISSING": "FilePartMissing",
        "FILE_REFERENCE_EMPTY": "FileReferenceEmpty",
        "FILE_REFERENCE_EXPIRED": "FileReferenceExpired",
        "FILE_REFERENCE_INVALID": "FileReferenceInvalid",
        "FILE_TITLE_EMPTY": "FileTitleEmpty",
        "FILTER_ID_INVALID": "FilterIdInvalid",
        "FILTER_INCLUDE_EMPTY": "FilterIncludeEmpty",
        "FILTER_NOT_SUPPORTED": "FilterNotSupported",
        "FILTER_TITLE_EMPTY": "FilterTitleEmpty",
        "FIRSTNAME_INVALID": "FirstnameInvalid",
        "FOLDER_ID_EMPTY": "FolderIdEmpty",
        "FOLDER_ID_INVALID": "FolderIdInvalid",
        "FORM_ID_EXPIRED": "FormIdExpired",
        "FRESH_CHANGE_ADMINS_FORBIDDEN": "FreshChangeAdminsForbidden",
        "FROM_MESSAGE_BOT_DISABLED": "FromMessageBotDisabled",
        "FROM_PEER_INVALID": "FromPeerInvalid",
        "GAME_BOT_INVALID": "GameBotInvalid",
        "GEO_POINT_INVALID": "GeoPointInvalid",
        "GIF_CONTENT_TYPE_INVALID": "GifContentTypeInvalid",
        "GIF_ID_INVALID": "GifIdInvalid",
        "GIFT_SLUG_EXPIRED": "GiftSlugExpired",
        "GRAPH_EXPIRED_RELOAD": "GraphExpiredReload",
        "GRAPH_INVALID_RELOAD": "GraphInvalidReload",
        "GRAPH_OUTDATED_RELOAD": "GraphOutdatedReload",
        "GROUPCALL_ALREADY_DISCARDED": "GroupcallAlreadyDiscarded",
        "GROUPCALL_INVALID": "GroupcallInvalid",
        "GROUPCALL_JOIN_MISSING": "GroupcallJoinMissing",
        "GROUPCALL_NOT_MODIFIED": "GroupcallNotModified",
        "GROUPCALL_SSRC_DUPLICATE_MUCH": "GroupcallSsrcDuplicateMuch",
        "GROUPED_MEDIA_INVALID": "GroupedMediaInvalid",
        "GROUP_CALL_INVALID": "GroupCallInvalid",
        "HASH_INVALID": "HashInvalid",
        "HIDE_REQUESTER_MISSING": "HideRequesterMissing",
        "IMAGE_PROCESS_FAILED": "ImageProcessFailed",
        "IMPORT_FILE_INVALID": "ImportFileInvalid",
        "IMPORT_FORMAT_UNRECOGNIZED": "ImportFormatUnrecognized",
        "IMPORT_ID_INVALID": "ImportIdInvalid",
        "INLINE_RESULT_EXPIRED": "InlineResultExpired",
        "INPUT_CONSTRUCTOR_INVALID": "InputConstructorInvalid",
        "INPUT_FETCH_ERROR": "InputFetchError",
        "INPUT_FETCH_FAIL": "InputFetchFail",
        "INPUT_FILTER_INVALID": "InputFilterInvalid",
        "INPUT_LAYER_INVALID": "InputLayerInvalid",
        "INPUT_METHOD_INVALID": "InputMethodInvalid",
        "INPUT_REQUEST_TOO_LONG": "InputRequestTooLong",
        "INPUT_TEXT_EMPTY": "InputTextEmpty",
        "INPUT_USER_DEACTIVATED": "InputUserDeactivated",
        "INVITE_FORBIDDEN_WITH_JOINAS": "InviteForbiddenWithJoinas",
        "INVITE_HASH_EMPTY": "InviteHashEmpty",
        "INVITE_HASH_EXPIRED": "InviteHashExpired",
        "INVITE_HASH_INVALID": "InviteHashInvalid",
        "INVITE_REQUEST_SENT": "InviteRequestSent",
        "INVITE_REVOKED_MISSING": "InviteRevokedMissing",
        "INVITE_SLUG_EMPTY": "InviteSlugEmpty",
        "INVITE_SLUG_EXPIRED": "InviteSlugExpired",
        "INVOICE_PAYLOAD_INVALID": "InvoicePayloadInvalid",
        "JOIN_AS_PEER_INVALID": "JoinAsPeerInvalid",
        "LANG_CODE_INVALID": "LangCodeInvalid",
        "LANG_CODE_NOT_SUPPORTED": "LangCodeNotSupported",
        "LANG_PACK_INVALID": "LangPackInvalid",
        "LASTNAME_INVALID": "LastnameInvalid",
        "LIMIT_INVALID": "LimitInvalid",
        "LINK_NOT_MODIFIED": "LinkNotModified",
        "LOCATION_INVALID": "LocationInvalid",
        "MAX_DATE_INVALID": "MaxDateInvalid",
        "MAX_ID_INVALID": "MaxIdInvalid",
        "MAX_QTS_INVALID": "MaxQtsInvalid",
        "MD5_CHECKSUM_INVALID": "Md5ChecksumInvalid",
        "MEDIA_CAPTION_TOO_LONG": "MediaCaptionTooLong",
        "MEDIA_EMPTY": "MediaEmpty",
        "MEDIA_FILE_INVALID": "MediaFileInvalid",
        "MEDIA_GROUPED_INVALID": "MediaGroupedInvalid",
        "MEDIA_INVALID": "MediaInvalid",
        "MEDIA_NEW_INVALID": "MediaNewInvalid",
        "MEDIA_PREV_INVALID": "MediaPrevInvalid",
        "MEDIA_TTL_INVALID": "MediaTtlInvalid",
        "MEDIA_VIDEO_STORY_MISSING": "MediaVideoStoryMissing",
        "MEGAGROUP_ID_INVALID": "MegagroupIdInvalid",
        "MEGAGROUP_PREHISTORY_HIDDEN": "MegagroupPrehistoryHidden",
        "MEGAGROUP_REQUIRED": "MegagroupRequired",
        "MESSAGE_EDIT_TIME_EXPIRED": "MessageEditTimeExpired",
        "MESSAGE_EMPTY": "MessageEmpty",
        "MESSAGE_IDS_EMPTY": "MessageIdsEmpty",
        "MESSAGE_ID_INVALID": "MessageIdInvalid",
        "MESSAGE_NOT_MODIFIED": "MessageNotModified",
        "MESSAGE_POLL_CLOSED": "MessagePollClosed",
        "MESSAGE_TOO_LONG": "MessageTooLong",
        "METHOD_INVALID": "MethodInvalid",
        "MIN_DATE_INVALID": "MinDateInvalid",
        "MSG_ID_INVALID": "MsgIdInvalid",
        "MSG_TOO_OLD": "MsgTooOld",
        "MSG_VOICE_MISSING": "MsgVoiceMissing",
        "MSG_WAIT_FAILED": "MsgWaitFailed",
        "MULTI_MEDIA_TOO_LONG": "MultiMediaTooLong",
        "NEW_SALT_INVALID": "NewSaltInvalid",
        "NEW_SETTINGS_EMPTY": "NewSettingsEmpty",
        "NEW_SETTINGS_INVALID": "NewSettingsInvalid",
        "NEXT_OFFSET_INVALID": "NextOffsetInvalid",
        "OFFSET_INVALID": "OffsetInvalid",
        "OFFSET_PEER_ID_INVALID": "OffsetPeerIdInvalid",
        "OPTIONS_TOO_MUCH": "OptionsTooMuch",
        "OPTION_INVALID": "OptionInvalid",
        "PACK_SHORT_NAME_INVALID": "PackShortNameInvalid",
        "PACK_SHORT_NAME_OCCUPIED": "PackShortNameOccupied",
        "PACK_TITLE_INVALID": "PackTitleInvalid",
        "PARTICIPANTS_TOO_FEW": "ParticipantsTooFew",
        "PARTICIPANT_ID_INVALID": "ParticipantIdInvalid",
        "PARTICIPANT_JOIN_MISSING": "ParticipantJoinMissing",
        "PARTICIPANT_VERSION_OUTDATED": "ParticipantVersionOutdated",
        "PASSWORD_EMPTY": "PasswordEmpty",
        "PASSWORD_HASH_INVALID": "PasswordHashInvalid",
        "PASSWORD_MISSING": "PasswordMissing",
        "PASSWORD_RECOVERY_NA": "PasswordRecoveryNa",
        "PASSWORD_REQUIRED": "PasswordRequired",
        "PASSWORD_TOO_FRESH_X": "PasswordTooFresh",
        "PAYMENT_PROVIDER_INVALID": "PaymentProviderInvalid",
        "PEER_FLOOD": "PeerFlood",
        "PEER_HISTORY_EMPTY": "PeerHistoryEmpty",
        "PEER_ID_INVALID": "PeerIdInvalid",
        "PEER_ID_NOT_SUPPORTED": "PeerIdNotSupported",
        "PERSISTENT_TIMESTAMP_EMPTY": "PersistentTimestampEmpty",
        "PERSISTENT_TIMESTAMP_INVALID": "PersistentTimestampInvalid",
        "PHONE_CODE_EMPTY": "PhoneCodeEmpty",
        "PHONE_CODE_EXPIRED": "PhoneCodeExpired",
        "PHONE_CODE_HASH_EMPTY": "PhoneCodeHashEmpty",
        "PHONE_CODE_INVALID": "PhoneCodeInvalid",
        "PHONE_HASH_EXPIRED": "PhoneHashExpired",
        "PHONE_NOT_OCCUPIED": "PhoneNotOccupied",
        "PHONE_NUMBER_APP_SIGNUP_FORBIDDEN": "PhoneNumberAppSignupForbidden",
        "PHONE_NUMBER_BANNED": "PhoneNumberBanned",
        "PHONE_NUMBER_FLOOD": "PhoneNumberFlood",
        "PHONE_NUMBER_INVALID": "PhoneNumberInvalid",
        "PHONE_NUMBER_OCCUPIED": "PhoneNumberOccupied",
        "PHONE_NUMBER_UNOCCUPIED": "PhoneNumberUnoccupied",
        "PHONE_PASSWORD_PROTECTED": "PhonePasswordProtected",
        "PHOTO_CONTENT_TYPE_INVALID": "PhotoContentTypeInvalid",
        "PHOTO_CONTENT_URL_EMPTY": "PhotoContentUrlEmpty",
        "PHOTO_CROP_FILE_MISSING": "PhotoCropFileMissing",
        "PHOTO_CROP_SIZE_SMALL": "PhotoCropSizeSmall",
        "PHOTO_EXT_INVALID": "PhotoExtInvalid",
        "PHOTO_FILE_MISSING": "PhotoFileMissing",
        "PHOTO_ID_INVALID": "PhotoIdInvalid",
        "PHOTO_INVALID": "PhotoInvalid",
        "PHOTO_INVALID_DIMENSIONS": "PhotoInvalidDimensions",
        "PHOTO_SAVE_FILE_INVALID": "PhotoSaveFileInvalid",
        "PHOTO_THUMB_URL_EMPTY": "PhotoThumbUrlEmpty",
        "PHOTO_THUMB_URL_INVALID": "PhotoThumbUrlInvalid",
        "PINNED_DIALOGS_TOO_MUCH": "PinnedDialogsTooMuch",
        "PIN_RESTRICTED": "PinRestricted",
        "POLL_ANSWERS_INVALID": "PollAnswersInvalid",
        "POLL_ANSWER_INVALID": "PollAnswerInvalid",
        "POLL_OPTION_DUPLICATE": "PollOptionDuplicate",
        "POLL_OPTION_INVALID": "PollOptionInvalid",
        "POLL_QUESTION_INVALID": "PollQuestionInvalid",
        "POLL_UNSUPPORTED": "PollUnsupported",
        "POLL_VOTE_REQUIRED": "PollVoteRequired",
        "PREMIUM_ACCOUNT_REQUIRED": "PremiumAccountRequired",
        "PRIVACY_KEY_INVALID": "PrivacyKeyInvalid",
        "PRIVACY_TOO_LONG": "PrivacyTooLong",
        "PRIVACY_VALUE_INVALID": "PrivacyValueInvalid",
        "PUBLIC_KEY_REQUIRED": "PublicKeyRequired",
        "QUERY_ID_EMPTY": "QueryIdEmpty",
        "QUERY_ID_INVALID": "QueryIdInvalid",
        "QUERY_TOO_SHORT": "QueryTooShort",
        "QUIZ_ANSWER_MISSING": "QuizAnswerMissing",
        "QUIZ_CORRECT_ANSWERS_EMPTY": "QuizCorrectAnswersEmpty",
        "QUIZ_CORRECT_ANSWERS_TOO_MUCH": "QuizCorrectAnswersTooMuch",
        "QUIZ_CORRECT_ANSWER_INVALID": "QuizCorrectAnswerInvalid",
        "QUIZ_MULTIPLE_INVALID": "QuizMultipleInvalid",
        "RANDOM_ID_EMPTY": "RandomIdEmpty",
        "RANDOM_ID_INVALID": "RandomIdInvalid",
        "RANDOM_LENGTH_INVALID": "RandomLengthInvalid",
        "RANGES_INVALID": "RangesInvalid",
        "REACTION_EMPTY": "ReactionEmpty",
        "REACTION_INVALID": "ReactionInvalid",
        "REFLECTOR_NOT_AVAILABLE": "ReflectorNotAvailable",
        "REPLY_MARKUP_BUY_EMPTY": "ReplyMarkupBuyEmpty",
        "REPLY_MARKUP_GAME_EMPTY": "ReplyMarkupGameEmpty",
        "REPLY_MARKUP_INVALID": "ReplyMarkupInvalid",
        "REPLY_MARKUP_TOO_LONG": "ReplyMarkupTooLong",
        "REPLY_MESSAGE_ID_INVALID": "ReplyMessageIdInvalid",
        "RESET_REQUEST_MISSING": "ResetRequestMissing",
        "RESULTS_TOO_MUCH": "ResultsTooMuch",
        "RESULT_ID_DUPLICATE": "ResultIdDuplicate",
        "RESULT_ID_EMPTY": "ResultIdEmpty",
        "RESULT_ID_INVALID": "ResultIdInvalid",
        "REACTIONS_TOO_MANY": "ReactionsTooMany",
        "RESULT_TYPE_INVALID": "ResultTypeInvalid",
        "REVOTE_NOT_ALLOWED": "RevoteNotAllowed",
        "RIGHTS_NOT_MODIFIED": "RightsNotModified",
        "RSA_DECRYPT_FAILED": "RsaDecryptFailed",
        "SCHEDULE_BOT_NOT_ALLOWED": "ScheduleBotNotAllowed",
        "SCHEDULE_DATE_INVALID": "ScheduleDateInvalid",
        "SCHEDULE_DATE_TOO_LATE": "ScheduleDateTooLate",
        "SCHEDULE_STATUS_PRIVATE": "ScheduleStatusPrivate",
        "SCHEDULE_TOO_MUCH": "ScheduleTooMuch",
        "SCORE_INVALID": "ScoreInvalid",
        "SEARCH_QUERY_EMPTY": "SearchQueryEmpty",
        "SEARCH_WITH_LINK_NOT_SUPPORTED": "SearchWithLinkNotSupported",
        "SECONDS_INVALID": "SecondsInvalid",
        "SEND_AS_PEER_INVALID": "SendAsPeerInvalid",
        "SEND_MESSAGE_MEDIA_INVALID": "SendMessageMediaInvalid",
        "SEND_MESSAGE_TYPE_INVALID": "SendMessageTypeInvalid",
        "SESSION_TOO_FRESH_X": "SessionTooFresh",
        "SETTINGS_INVALID": "SettingsInvalid",
        "SHA256_HASH_INVALID": "Sha256HashInvalid",
        "SHORTNAME_OCCUPY_FAILED": "ShortnameOccupyFailed",
        "SHORT_NAME_INVALID": "ShortNameInvalid",
        "SHORT_NAME_OCCUPIED": "ShortNameOccupied",
        "SLOWMODE_MULTI_MSGS_DISABLED": "SlowmodeMultiMsgsDisabled",
        "SMS_CODE_CREATE_FAILED": "SmsCodeCreateFailed",
        "SRP_ID_INVALID": "SrpIdInvalid",
        "SRP_PASSWORD_CHANGED": "SrpPasswordChanged",
        "START_PARAM_EMPTY": "StartParamEmpty",
        "START_PARAM_INVALID": "StartParamInvalid",
        "START_PARAM_TOO_LONG": "StartParamTooLong",
        "STICKERPACK_STICKERS_TOO_MUCH": "StickerpackStickersTooMuch",
        "STICKERSET_INVALID": "StickersetInvalid",
        "STICKERSET_NOT_MODIFIED": "StickersetNotModified",
        "STICKERS_EMPTY": "StickersEmpty",
        "STICKERS_TOO_MUCH": "StickersTooMuch",
        "STICKER_DOCUMENT_INVALID": "StickerDocumentInvalid",
        "STICKER_EMOJI_INVALID": "StickerEmojiInvalid",
        "STICKER_FILE_INVALID": "StickerFileInvalid",
        "STICKER_GIF_DIMENSIONS": "StickerGifDimensions",
        "STICKER_ID_INVALID": "StickerIdInvalid",
        "STICKER_INVALID": "StickerInvalid",
        "STICKER_MIME_INVALID": "StickerMimeInvalid",
        "STICKER_PNG_DIMENSIONS": "StickerPngDimensions",
        "STICKER_PNG_NOPNG": "StickerPngNopng",
        "STICKER_TGS_NODOC": "StickerTgsNodoc",
        "STICKER_TGS_NOTGS": "StickerTgsNotgs",
        "STICKER_THUMB_PNG_NOPNG": "StickerThumbPngNopng",
        "STICKER_VIDEO_BIG": "StickerVideoBig",
        "STICKER_VIDEO_NODOC": "StickerVideoNodoc",
        "STICKER_VIDEO_NOWEBM": "StickerVideoNowebm",
        "STORIES_TOO_MUCH": "StoriesTooMuch",
        "STORY_PERIOD_INVALID": "StoryPeriodInvalid",
        "SWITCH_PM_TEXT_EMPTY": "SwitchPmTextEmpty",
        "TAKEOUT_INVALID": "TakeoutInvalid",
        "TAKEOUT_REQUIRED": "TakeoutRequired",
        "TEMP_AUTH_KEY_ALREADY_BOUND": "TempAuthKeyAlreadyBound",
        "TEMP_AUTH_KEY_EMPTY": "TempAuthKeyEmpty",
        "THEME_FILE_INVALID": "ThemeFileInvalid",
        "THEME_FORMAT_INVALID": "ThemeFormatInvalid",
        "THEME_INVALID": "ThemeInvalid",
        "THEME_MIME_INVALID": "ThemeMimeInvalid",
        "THEME_TITLE_INVALID": "ThemeTitleInvalid",
        "TITLE_INVALID": "TitleInvalid",
        "TMP_PASSWORD_DISABLED": "TmpPasswordDisabled",
        "TMP_PASSWORD_INVALID": "TmpPasswordInvalid",
        "TOKEN_INVALID": "TokenInvalid",
        "TOPIC_CLOSED": "TopicClosed",
        "TOPIC_DELETED": "TopicDeleted",
        "TOPIC_ID_INVALID": "TopicIdInvalid",
        "TOPIC_NOT_MODIFIED": "TopicNotModified",
        "TO_LANG_INVALID": "ToLangInvalid",
        "TRANSCRIPTION_FAILED": "TranscriptionFailed",
        "TTL_DAYS_INVALID": "TtlDaysInvalid",
        "TTL_MEDIA_INVALID": "TtlMediaInvalid",
        "TYPES_EMPTY": "TypesEmpty",
        "TYPE_CONSTRUCTOR_INVALID": "TypeConstructorInvalid",
        "UNKNOWN_ERROR": "UnknownError",
        "UNTIL_DATE_INVALID": "UntilDateInvalid",
        "URL_INVALID": "UrlInvalid",
        "USAGE_LIMIT_INVALID": "UsageLimitInvalid",
        "USERNAME_INVALID": "UsernameInvalid",
        "USERNAME_NOT_MODIFIED": "UsernameNotModified",
        "USERNAME_NOT_OCCUPIED": "UsernameNotOccupied",
        "USERNAME_OCCUPIED": "UsernameOccupied",
        "USERNAME_PURCHASE_AVAILABLE": "UsernamePurchaseAvailable",
        "USERPIC_UPLOAD_REQUIRED": "UserpicUploadRequired",
        "USERS_TOO_FEW": "UsersTooFew",
        "USERS_TOO_MUCH": "UsersTooMuch",
        "USER_ADMIN_INVALID": "UserAdminInvalid",
        "USER_ALREADY_INVITED": "UserAlreadyInvited",
        "USER_ALREADY_PARTICIPANT": "UserAlreadyParticipant",
        "USER_BANNED_IN_CHANNEL": "UserBannedInChannel",
        "USER_BLOCKED": "UserBlocked",
        "USER_BOT": "UserBot",
        "USER_BOT_INVALID": "UserBotInvalid",
        "USER_BOT_REQUIRED": "UserBotRequired",
        "USER_CHANNELS_TOO_MUCH": "UserChannelsTooMuch",
        "USER_CREATOR": "UserCreator",
        "USER_ID_INVALID": "UserIdInvalid",
        "USER_INVALID": "UserInvalid",
        "USER_IS_BLOCKED": "UserIsBlocked",
        "USER_IS_BOT": "UserIsBot",
        "USER_KICKED": "UserKicked",
        "USER_NOT_MUTUAL_CONTACT": "UserNotMutualContact",
        "USER_NOT_PARTICIPANT": "UserNotParticipant",
        "USER_PUBLIC_MISSING": "UserPublicMissing",
        "USER_VOLUME_INVALID": "UserVolumeInvalid",
        "VIDEO_CONTENT_TYPE_INVALID": "VideoContentTypeInvalid",
        "VIDEO_FILE_INVALID": "VideoFileInvalid",
        "VIDEO_TITLE_EMPTY": "VideoTitleEmpty",
        "VOICE_MESSAGES_FORBIDDEN": "VoiceMessagesForbidden",
        "VOLUME_LOC_NOT_FOUND": "VolumeLocNotFound",
        "WALLPAPER_FILE_INVALID": "WallpaperFileInvalid",
        "WALLPAPER_INVALID": "WallpaperInvalid",
        "WALLPAPER_MIME_INVALID": "WallpaperMimeInvalid",
        "WC_CONVERT_URL_INVALID": "WcConvertUrlInvalid",
        "WEBDOCUMENT_INVALID": "WebdocumentInvalid",
        "WEBDOCUMENT_MIME_INVALID": "WebdocumentMimeInvalid",
        "WEBDOCUMENT_SIZE_TOO_BIG": "WebdocumentSizeTooBig",
        "WEBDOCUMENT_URL_EMPTY": "WebdocumentUrlEmpty",
        "WEBDOCUMENT_URL_INVALID": "WebdocumentUrlInvalid",
        "WEBPAGE_CURL_FAILED": "WebpageCurlFailed",
        "WEBPAGE_MEDIA_EMPTY": "WebpageMediaEmpty",
        "WEBPAGE_NOT_FOUND": "WebpageNotFound",
        "WEBPAGE_URL_INVALID": "WebpageUrlInvalid",
        "WEBPUSH_AUTH_INVALID": "WebpushAuthInvalid",
        "WEBPUSH_KEY_INVALID": "WebpushKeyInvalid",
        "WEBPUSH_TOKEN_INVALID": "WebpushTokenInvalid",
        "YOU_BLOCKED_USER": "YouBlockedUser",
        "STORIES_NEVER_CREATED": "StoriesNeverCreated",
        "MEDIA_FILE_INVALID": "MediaFileInvalid",
        "CHANNEL_FORUM_MISSING": "ChannelForumMissing",
        "TTL_PERIOD_INVALID": "TtlPeriodInvalid",
        "BOOSTS_REQUIRED": "BoostsRequired",
        "BOOSTS_EMPTY": "BoostsEmpty",
    },
    420: {
        "_": "Flood",
        "2FA_CONFIRM_WAIT_X": "TwoFaConfirmWait",
        "FLOOD_TEST_PHONE_WAIT_X": "FloodTestPhoneWait",
        "FLOOD_WAIT_X": "FloodWait",
        "FLOOD_PREMIUM_WAIT_X": "FloodPremiumWait",
        "PREMIUM_SUB_ACTIVE_UNTIL_X": "PremiumSubActiveUntil",
        "SLOWMODE_WAIT_X": "SlowmodeWait",
        "STORY_SEND_FLOOD_X": "StorySendFlood",
        "TAKEOUT_INIT_DELAY_X": "TakeoutInitDelay",
    },
}
