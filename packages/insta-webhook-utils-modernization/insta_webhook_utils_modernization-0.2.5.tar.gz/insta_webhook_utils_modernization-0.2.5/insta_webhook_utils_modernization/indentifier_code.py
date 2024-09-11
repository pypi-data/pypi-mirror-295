import json
import traceback
from enum import Enum
from typing import Dict, Any, Optional, List


class InstaChannelsEnum(Enum):
    InstagramPagePosts = 20
    InstagramUserPosts = 21
    InstagramComments = 22
    InstagramPublicPosts = 23
    InstagramMessages = 70


class InstaPostChannelType(Enum):
    BRAND = 1
    MENTION = 2
    PUBLIC = 3
    STORIES = 4
    DUMMY_POST = 5
    TAGS = 6
    IGTV = 7
    REELS = 8
    ADS = 9
    REVIEWS = 10
    STORIES_MENTION = 11
    RECOMMENDATION = 12


class InstagramEventType(Enum):
    COMMENT_ON_REEL = "comment_on_reel"
    COMMENT_ON_FEED = "comment_on_feed"
    COMMENT_REPLY_ON_FEED = "comment_reply_on_feed"
    COMMENT_ON_AD = "comment_on_ad"
    MENTION_IN_COMMENT = "mention_in_comment"
    STORY_MENTION = "story_mention"
    MESSAGE = "message"
    MESSAGE_READ = "message_read"
    MESSAGE_WITH_VIDEO = "message_with_video"
    UNSUPPORTED_ATTACHMENT = "unsupported_attachment"
    STORY_INSIGHTS = "story_insights"
    MENTION_IN_FEED = "mention_in_feed"
    STANDBY_READ = "standby_read"
    STANDBY_REPLY_TO_MESSAGE = "standby_reply_to_message"
    STANDBY_SIMPLE_MESSAGE = "standby_simple_message"
    PASS_THREAD_CONTROL = "pass_thread_control"
    STANDBY_TAKE_THREAD_CONTROL = "standby_take_thread_control"
    MENTION_IN_MEDIA = "mention_in_media"
    MESSAGE_REACT = "message_react"
    MESSAGE_UNREACT = "message_unreact"
    STANDBY_MESSAGE_WITH_IMAGE = "standby_message_with_image"
    STANDBY_MESSAGE_WITH_VIDEO = "standby_message_with_video"
    STANDBY_MESSAGE_WITH_UNSUPPORTED_ATTACHMENT = "standby_message_with_unsupported_attachment"
    STANDBY_REACTION = "standby_reaction"
    STANDBY_MESSAGE_WITH_SHARE = "standby_message_with_share"
    STANDBY_MESSAGE_WITH_REEL = "standby_message_with_reel"
    STANDBY_STORY_MENTION = "standby_story_mention"
    STANDBY_MESSAGE_DELETED = "standby_message_deleted"
    STANDBY_MESSAGE_WITH_AUDIO = "standby_message_with_audio"
    POSTBACK = "postback"
    REQUEST_THREAD_CONTROL = "request_thread_control"


def process_media_event(changes_value: Dict[str, Any]) -> Optional[InstagramEventType]:
    """Process media-related events like comments or mentions using a mapping approach."""

    media_type = changes_value.get('media', {}).get('media_product_type')

    # Mapping media types to InstagramEventType
    media_type_mapping = {
        'REELS': InstagramEventType.COMMENT_ON_REEL,
        'FEED': InstagramEventType.COMMENT_ON_FEED,
        'AD': InstagramEventType.COMMENT_ON_AD
    }

    # Check if media_type exists in the mapping
    if media_type == 'FEED' and 'parent_id' in changes_value:
        return InstagramEventType.COMMENT_REPLY_ON_FEED

    return media_type_mapping.get(media_type.upper() if media_type else None)


def process_mentions_event(changes_value: Dict[str, Any], changes_field: str) -> Optional[InstagramEventType]:
    """Process mention-related events."""
    if changes_field == 'mentions':
        if 'comment_id' in changes_value:
            return InstagramEventType.MENTION_IN_COMMENT
        return InstagramEventType.MENTION_IN_MEDIA
    return None


def process_messaging_event(message_value: Dict[str, Any]) -> Optional[InstagramEventType]:
    """Process messaging-related events using a mapping approach."""

    # Map message keys to their corresponding event types
    event_mapping: Dict[str, InstagramEventType] = {
        'postback': InstagramEventType.POSTBACK,
        'pass_thread_control': InstagramEventType.PASS_THREAD_CONTROL,
        'request_thread_control': InstagramEventType.REQUEST_THREAD_CONTROL,
        'read': InstagramEventType.MESSAGE_READ
    }

    # Check if any direct events are present
    for key, event_type in event_mapping.items():
        if key in message_value:
            return event_type

    # Map reaction actions to event types
    reaction: Dict[str, Any] = message_value.get('reaction', {})
    reaction_mapping: Dict[str, InstagramEventType] = {
        'react': InstagramEventType.MESSAGE_REACT,
        'unreact': InstagramEventType.MESSAGE_UNREACT
    }
    if 'action' in reaction:
        return reaction_mapping.get(reaction['action'])

    # Map attachment types to event types
    attachment_mapping: Dict[str, InstagramEventType] = {
        'video': InstagramEventType.MESSAGE_WITH_VIDEO,
        'unsupported_type': InstagramEventType.UNSUPPORTED_ATTACHMENT,
        'story_mention': InstagramEventType.STORY_MENTION
    }

    attachments: List[Dict[str, Any]] = message_value.get('message', {}).get('attachments', [])
    for attachment in attachments:
        attachment_type: Optional[str] = attachment.get('type')
        if attachment_type in attachment_mapping:
            return attachment_mapping[attachment_type]

    # Return MESSAGE type if 'message' exists in the payload
    return InstagramEventType.MESSAGE if 'message' in message_value else None


def process_standby_event(standby_value: Dict[str, Any]) -> Optional[InstagramEventType]:
    """Process standby-related events using a mapping approach."""

    # Map direct event keys to their corresponding event types
    event_mapping: Dict[str, InstagramEventType] = {
        'reaction': InstagramEventType.STANDBY_REACTION,
        'read': InstagramEventType.STANDBY_READ,
        'take_thread_control': InstagramEventType.STANDBY_TAKE_THREAD_CONTROL
    }

    # Check for direct events
    for key, event_type in event_mapping.items():
        if key in standby_value:
            return event_type

    # Check for message-related events
    message: Dict[str, Any] = standby_value.get('message', {})

    message_mapping: Dict[str, InstagramEventType] = {
        'reply_to': InstagramEventType.STANDBY_REPLY_TO_MESSAGE,
        'is_deleted': InstagramEventType.STANDBY_MESSAGE_DELETED,
        'text': InstagramEventType.STANDBY_SIMPLE_MESSAGE
    }

    for key, event_type in message_mapping.items():
        if key in message:
            return event_type

    # Process standby attachments
    attachments: List[Dict[str, Any]] = message.get('attachments', [])
    attachment_mapping: Dict[str, InstagramEventType] = {
        'image': InstagramEventType.STANDBY_MESSAGE_WITH_IMAGE,
        'video': InstagramEventType.STANDBY_MESSAGE_WITH_VIDEO,
        'unsupported_type': InstagramEventType.STANDBY_MESSAGE_WITH_UNSUPPORTED_ATTACHMENT,
        'share': InstagramEventType.STANDBY_MESSAGE_WITH_SHARE,
        'ig_reel': InstagramEventType.STANDBY_MESSAGE_WITH_REEL,
        'story_mention': InstagramEventType.STANDBY_STORY_MENTION,
        'audio': InstagramEventType.STANDBY_MESSAGE_WITH_AUDIO
    }

    for attachment in attachments:
        attachment_type: Optional[str] = attachment.get('type')
        if attachment_type in attachment_mapping:
            return attachment_mapping[attachment_type]

    return None


def classify_instagram_event(event_data):
    """Classify Instagram events based on the event data."""
    event = json.loads(event_data) if isinstance(event_data, str) else event_data
    try:
        changes = event.get('entry', [{}])[0]

        # Check if changes field exists
        changes_list = changes.get('changes', [{}])
        changes_field = changes_list[0].get('field', '')
        changes_value = changes_list[0].get('value', {})

        # Check for story insights
        if changes_field == 'story_insights':
            return InstagramEventType.STORY_INSIGHTS

        # Process media events
        media_event = process_media_event(changes_value)
        if media_event:
            return media_event

        # Process mentions
        mentions_event = process_mentions_event(changes_value, changes_field)
        if mentions_event:
            return mentions_event

        # Process messaging events
        if 'messaging' in changes:
            return process_messaging_event(changes['messaging'][0])

        # Process standby events
        if 'standby' in changes:
            return process_standby_event(changes['standby'][0])

        return None  # Return None if no match is found

    except KeyError as e:
        traceback.print_exc()
        print(f"KeyError: {e} for event is: {event}")
        return None
    except Exception as e:
        traceback.print_exc()
        print(f"Exception: {e} for event is: {event}")
        return None
