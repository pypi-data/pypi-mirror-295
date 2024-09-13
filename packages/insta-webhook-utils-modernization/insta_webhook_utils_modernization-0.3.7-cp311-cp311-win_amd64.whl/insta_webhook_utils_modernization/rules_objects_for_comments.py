from datetime import datetime

from insta_webhook_utils_modernization.common_functions import get_media_type
from insta_webhook_utils_modernization.indentifier_code import InstaPostChannelType


def handle_media_type(value, **kwargs):
    return get_media_type(value)


def url_handler(value, **kwargs):
    if not value:
        screen_name = kwargs.get("data").get("comment_username")
        if not screen_name:
            screen_name = kwargs.get("data").get("post_username")
        url = f"https://www.instagram.com/{screen_name}/"
        return url
    return ""


def handle_post_type_for_comment(value, **kwargs):
    comment_author_id = kwargs['data'].get('comment_author_id')
    if not comment_author_id:
        comment_author_id = 0
    is_brand_post = int(kwargs['data']['author_social_id']) == int(comment_author_id)
    if is_brand_post:
        return InstaPostChannelType.BRAND.value
    return InstaPostChannelType.PUBLIC.value


def comment_url_creator(value, **kwargs):
    # Assuming the necessary variables are defined
    type_of_reply = kwargs.get('data', {}).get('type_of', 0)

    comment_id = kwargs['data'].get('post_id', '')
    post_url = kwargs['data'].get('parent_post_url', '')
    if type_of_reply == 1:
        return post_url
    # Check if comment_id is not empty and update the PostURL
    if comment_id:
        comment_url = f"{post_url}c/{comment_id}"
    else:
        comment_url = post_url

    # If the PostURL doesn't contain 'instagram', set it to the default URL
    if 'instagram' not in comment_url:
        comment_url = "https://www.instagram.com/p/0000000000000/"

    return comment_url


def dynamic_attachment_handler(value, **kwargs):
    return value


def comment_post_time_handler(value, **kwargs):
    if isinstance(value, str):
        return value
    dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


def utc_time_to_iso_format(current_time=None, **kwargs):
    return datetime.utcnow().isoformat()


def comment_post_description_handler(value, **kwargs):
    if value:
        return value.replace("\n", " ").replace("\r", " ")
    return ""


def comment_post_is_brand_post_handler(setting_author_id, **kwargs):
    comment_author_id = kwargs['data'].get('post_author_id')
    if not comment_author_id:
        comment_author_id = 0
    if int(setting_author_id) == comment_author_id:
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
        "keys": ["comment_time"],
        "default_value": datetime.utcnow,
        "handler_function": comment_post_time_handler,
        "clickhouse_column_name": "created_date",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.Url": {
        "keys": ["permalink"],
        "default_value": "",
        "handler_function": comment_url_creator,
        "clickhouse_column_name": "url",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.SocialID": {
        "keys": ["post_id"],
        "default_value": None,
        "handler_function": None,
        "clickhouse_column_name": "tweetidorfbid",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.InstagramGraphApiID": {
        "keys": ["post_id"],
        "default_value": None,
        "handler_function": None,
        "clickhouse_column_name": "InstagramGraphApiID",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.PostSocialID": {
        "keys": ["parent_post_social_id"],
        "default_value": None,
        "handler_function": None,
        "clickhouse_column_name": "postsocialid",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.Description": {
        "keys": ["comment_text"],
        "default_value": "",
        "handler_function": comment_post_description_handler,
        "clickhouse_column_name": "description",
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
        "keys": ["comment_likes_count"],
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
        "keys": ['comment_follower_count'],
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
        "keys": ["permalink"],
        "default_value": "",
        "handler_function": comment_url_creator,
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
        "keys": ["comment_text"],
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
        "keys": ["attachment_xml"],
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
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "isBrandPost": {
        "keys": ["author_social_id"],
        "default_value": 0,
        "handler_function": comment_post_is_brand_post_handler,
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
        "default_value": "instagram_utils_comment_modernization",
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
        "keys": ["post_username", "comment_username"],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.AuthorName": {
        "keys": ["post_username", "comment_username"],
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
        "keys": ["comment_profile_picture"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.UserInfo.Url": {
        "keys": [],
        "default_value": "",
        "handler_function": url_handler,
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
        "keys": ["post_author_id"],
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
        "keys": ["comment_follows_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.FollowersCount": {
        "keys": ["comment_follower_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": True,
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
        "keys": ["comment_tweet_count"],
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
