# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Updates = Union["raw.types.UpdateShort", "raw.types.UpdateShortChatMessage", "raw.types.UpdateShortMessage", "raw.types.UpdateShortSentMessage", "raw.types.Updates", "raw.types.UpdatesCombined", "raw.types.UpdatesTooLong"]


class Updates:  # type: ignore
    """Object which is perceived by the client without a call on its part when an event occurs.

    Constructors:
        This base type has 7 constructors available.

        .. currentmodule:: pyrogram.raw.types

        .. autosummary::
            :nosignatures:

            UpdateShort
            UpdateShortChatMessage
            UpdateShortMessage
            UpdateShortSentMessage
            Updates
            UpdatesCombined
            UpdatesTooLong

    Functions:
        This object can be returned by 105 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetNotifyExceptions
            account.UpdateConnectedBot
            account.GetBotBusinessConnection
            contacts.DeleteContacts
            contacts.AddContact
            contacts.AcceptContact
            contacts.GetLocated
            contacts.BlockFromReplies
            messages.SendMessage
            messages.SendMedia
            messages.ForwardMessages
            messages.EditChatTitle
            messages.EditChatPhoto
            messages.DeleteChatUser
            messages.ImportChatInvite
            messages.StartBot
            messages.MigrateChat
            messages.SendInlineBotResult
            messages.EditMessage
            messages.GetAllDrafts
            messages.SetGameScore
            messages.SendScreenshotNotification
            messages.SendMultiMedia
            messages.UpdatePinnedMessage
            messages.SendVote
            messages.GetPollResults
            messages.EditChatDefaultBannedRights
            messages.SendScheduledMessages
            messages.DeleteScheduledMessages
            messages.SetHistoryTTL
            messages.SetChatTheme
            messages.HideChatJoinRequest
            messages.HideAllChatJoinRequests
            messages.ToggleNoForwards
            messages.SendReaction
            messages.GetMessagesReactions
            messages.SetChatAvailableReactions
            messages.SendWebViewData
            messages.GetExtendedMedia
            messages.SendBotRequestedPeer
            messages.SetChatWallPaper
            messages.SendQuickReplyMessages
            messages.DeleteQuickReplyMessages
            messages.EditFactCheck
            messages.DeleteFactCheck
            messages.SendPaidReaction
            messages.GetPaidReactionPrivacy
            channels.CreateChannel
            channels.EditAdmin
            channels.EditTitle
            channels.EditPhoto
            channels.JoinChannel
            channels.LeaveChannel
            channels.DeleteChannel
            channels.ToggleSignatures
            channels.EditBanned
            channels.DeleteHistory
            channels.TogglePreHistoryHidden
            channels.EditCreator
            channels.ToggleSlowMode
            channels.ConvertToGigagroup
            channels.ToggleJoinToSend
            channels.ToggleJoinRequest
            channels.ToggleForum
            channels.CreateForumTopic
            channels.EditForumTopic
            channels.UpdatePinnedForumTopic
            channels.ReorderPinnedForumTopics
            channels.ToggleAntiSpam
            channels.ToggleParticipantsHidden
            channels.UpdateColor
            channels.ToggleViewForumAsMessages
            channels.UpdateEmojiStatus
            channels.SetBoostsToUnblockRestrictions
            channels.RestrictSponsoredMessages
            bots.AllowSendMessage
            payments.AssignAppStoreTransaction
            payments.AssignPlayMarketTransaction
            payments.ApplyGiftCode
            payments.LaunchPrepaidGiveaway
            payments.RefundStarsCharge
            phone.DiscardCall
            phone.SetCallRating
            phone.CreateGroupCall
            phone.JoinGroupCall
            phone.LeaveGroupCall
            phone.InviteToGroupCall
            phone.DiscardGroupCall
            phone.ToggleGroupCallSettings
            phone.ToggleGroupCallRecord
            phone.EditGroupCallParticipant
            phone.EditGroupCallTitle
            phone.ToggleGroupCallStartSubscription
            phone.StartScheduledGroupCall
            phone.JoinGroupCallPresentation
            phone.LeaveGroupCallPresentation
            folders.EditPeerFolders
            chatlists.JoinChatlistInvite
            chatlists.JoinChatlistUpdates
            chatlists.LeaveChatlist
            stories.SendStory
            stories.EditStory
            stories.ActivateStealthMode
            stories.SendReaction
            stories.GetAllReadPeerStories
    """

    QUALNAME = "pyrogram.raw.base.Updates"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
