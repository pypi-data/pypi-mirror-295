import html
from datetime import datetime

from insta_webhook_utils_modernization.common_functions import get_media_type
from insta_webhook_utils_modernization.indentifier_code import InstaChannelsEnum, InstaPostChannelType


def handle_media_type(value, **kwargs):
    return get_media_type(value)


def handler_for_post_type_parent(value, **kwargs):
    try:
        author_id_acc = int(kwargs['data']['author_social_id'])
        post_owner_id = int(kwargs['data']['owner']['id'])
        is_brand_post = author_id_acc == post_owner_id
        if is_brand_post:
            return InstaPostChannelType.BRAND.value
        elif value and value.upper() == "AD":
            return InstaPostChannelType.ADS.value
        elif value and value.upper() == "STORIES_MENTION":
            return InstaPostChannelType.STORIES_MENTION.value
        elif value and value.upper() == "REELS":
            return InstaPostChannelType.REELS.value
        elif value and value.upper() == "IGTV":
            return InstaPostChannelType.IGTV.value
        elif value and value.upper() == "TAGS":
            return InstaPostChannelType.TAGS.value
        return InstaPostChannelType.BRAND.value
    except Exception as e:
        return InstaPostChannelType.BRAND.value


def handler_for_dark_post(value, **kwargs):
    try:
        if value and value.upper() == "AD":
            return True
        return False
    except Exception as e:
        return False


def parent_chanel_handler(value, **kwargs):
    author_id_acc = int(kwargs['data']['author_social_id'])
    post_owner_id = int(kwargs['data']['owner']['id'])
    is_brand_post = author_id_acc == post_owner_id
    if is_brand_post:
        return InstaChannelsEnum.InstagramPagePosts.value
    return InstaChannelsEnum.InstagramPublicPosts.value


def escape_url(url):
    # Escape special characters in the URL
    return html.escape(url)


def dynamic_attachment_handler(value, **kwargs):
    main_data = kwargs.get("data")
    if isinstance(value, list):
        attachments = "<Attachments>"
        for item in value:
            try:
                item_str = (
                    "<Item>"
                    f"<Name>{item['media_type']}</Name>"
                    f"<MediaType>{get_media_type(item['media_type'])}</MediaType>"
                    f"<ThumbUrl>{escape_url(item['media_url'])}</ThumbUrl>"
                    f"<Url>{escape_url(item['media_url'])}</Url>"
                    "</Item>"
                )
                attachments += item_str
            except Exception as e:
                pass
        if attachments == "<Attachments>":
            return ""
        attachments += "</Attachments>"
        return attachments
    if main_data:
        thumb_url = main_data.get("thumbnail_url", "")
        media_url = main_data.get("permalink", "")
        media_type = get_media_type(main_data.get('media_type'))
        return f"""<Attachments><Item><Name>{main_data.get('media_type')}</Name><MediaType>{media_type}</MediaType><ThumbUrl>{escape_url(thumb_url)}</ThumbUrl><Url>{media_url}</Url></Item></<Attachments>"""
    return value


def parent_post_time_handler(value, **kwargs):
    dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


def utc_time_to_iso_format(current_time=None, **kwargs):
    return datetime.utcnow().isoformat()


def parent_post_description_handler(value, **kwargs):
    if value:
        return value.replace("\n", " ").replace("\r", " ")
    return ""


def parent_post_is_brand_post_handler(setting_author_id, **kwargs):
    if int(setting_author_id) == int(kwargs['data']['owner']['id']):
        return True
    return False


rules_obj = {
    "RawData.SettingID": {
        "keys": ["setting_id"],
        "default_value": None,
        "handler_function": None,
        "clickhouse_column_name": "settingid",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.CreatedDate": {
        "keys": ["timestamp"],
        "default_value": datetime.utcnow,
        "handler_function": parent_post_time_handler,
        "clickhouse_column_name": "created_date",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.Url": {
        "keys": ["permalink"],
        "default_value": "",
        "handler_function": None,
        "clickhouse_column_name": "url",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.SocialID": {
        "keys": ["id"],
        "default_value": None,
        "handler_function": None,
        "clickhouse_column_name": "tweetidorfbid",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.Description": {
        "keys": ["description", "caption"],
        "default_value": "",
        "handler_function": parent_post_description_handler,
        "clickhouse_column_name": "description",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.isDarkPost": {
        "keys": ["media_product_type"],
        "default_value": "",
        "handler_function": handler_for_dark_post,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.LanguageName": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.Lang": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.Hastagcloud": {
        "keys": [],
        "default_value": [],
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.CountryCode": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.NumCommentsCount": {
        "keys": ["comments_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": False
    },
    "RawData.NumLikesCount": {
        "keys": ["like_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": False
    },
    "RawData.PostInsights": {
        "keys": [],
        "default_value": {},
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True

    },
    "RawData.NumLikesORFollowers": {
        "keys": ["owner.followers_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": False
    },
    "RawData.NumVideoViews": {
        "keys": [],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.NumShareCount": {
        "keys": [],
        "default_value": 0,
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.DurationInSeconds": {
        "keys": [],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.ShareURL": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "clickhouse_column_name": "m_share_url",
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.PostPermissions": {
        "keys": [],
        "default_value": [],
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.SimplifiedText": {
        "keys": ["description"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.VideoDetails": {
        "keys": [],
        "default_value": [],
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.MusicDetails": {
        "keys": [],
        "default_value": [],
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True

    },
    "RawData.AttachmentXML": {
        "keys": ["children.data", "AttachmentXML"],
        "default_value": "",
        "handler_function": dynamic_attachment_handler,
        "mandatory": False,
        "skip_if_missing": False
    },
    "RawData.MediaType": {
        "keys": ["media_type"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False

    },
    "RawData.MediaEnum": {
        "keys": ["media_type"],
        "default_value": "",
        "handler_function": handle_media_type,
        "mandatory": True,
        "skip_if_missing": False

    },
    "RawData.Posttype": {
        "keys": ["media_product_type"],
        "default_value": "",
        "handler_function": handler_for_post_type_parent,
        "mandatory": False,
        "skip_if_missing": True
    },
    "ChannelGroup": {
        "keys": ["channel_group_id"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "ChannelType": {
        "keys": ["channel_type"],
        "default_value": "",
        "handler_function": parent_chanel_handler,
        "mandatory": True,
        "skip_if_missing": False
    },
    "isBrandPost": {
        "keys": ["author_social_id"],
        "default_value": 0,
        "handler_function": parent_post_is_brand_post_handler,
        "mandatory": True,
        "skip_if_missing": False
    },
    "BrandInfo.BrandID": {
        "keys": ["brand_id"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "BrandInfo.BrandName": {
        "keys": ["brand_name"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "BrandInfo.CategoryID": {
        "keys": ["category_id"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "BrandInfo.CategoryName": {
        "keys": ["category_name"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "BrandInfo.BrandSettings": {
        "keys": [],
        "default_value": {},
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "BrandInfo.OperationEnum": {
        "keys": [],
        "default_value": None,
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "ServiceName": {
        "keys": [],
        "default_value": "instagram_utils_parent_modernization",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "MentionTrackingDetails.FetchingServiceInTime": {
        "keys": ["in_time"],
        "default_value": datetime.utcnow().isoformat(),
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "MentionTrackingDetails.FetchingServiceOutTime": {
        "keys": [],
        "default_value": "",
        "handler_function": utc_time_to_iso_format,
        "mandatory": True,
        "skip_if_missing": False
    },
    # User Model Rules Start Here
    "RawData.UserInfo.ScreenName": {
        "keys": ["username"],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.AuthorName": {
        "keys": ["owner.name"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.UserInfo.ScreenNameModifiedDate": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.Gender": {
        "keys": [],
        "default_value": -1,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.PicUrl": {
        "keys": ["owner.profile_picture_url"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.UserInfo.Url": {
        "keys": ["owner.website"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.UserInfo.UpdatedDate": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.IsVerified": {
        "keys": [],
        "default_value": False,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.LanguageJson": {
        "keys": [],
        "default_value": False,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.AuthorSocialID": {
        "keys": ["owner.id"],
        "default_value": False,
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.UserInfo.IsMuted": {
        "keys": [],
        "default_value": False,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.FollowingCount": {
        "keys": ["owner.follows_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.FollowersCount": {
        "keys": ["owner.followers_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.Insights": {
        "keys": [],
        "default_value": {},
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.TweetCount": {
        "keys": ["owner.media_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.IsBlocked": {
        "keys": [],
        "default_value": False,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.IsHidden": {
        "keys": [],
        "default_value": False,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.IsUserPrivate": {
        "keys": [],
        "default_value": False,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.SocialChannels": {
        "keys": [],
        "default_value": [],
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.ChannelGroupID": {
        "keys": ["channel_group_id"],
        "default_value": None,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.Location.country": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.Location.country_code": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.Location.locationname": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    }
}
