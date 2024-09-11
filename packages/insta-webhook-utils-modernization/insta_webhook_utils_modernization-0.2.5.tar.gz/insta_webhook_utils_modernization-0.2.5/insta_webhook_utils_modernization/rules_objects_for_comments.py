from datetime import datetime

from insta_webhook_utils_modernization.common_functions import get_media_type
from insta_webhook_utils_modernization.indentifier_code import InstaPostChannelType


def handle_media_type(value, **kwargs):
    return get_media_type(value)


def handle_post_type_for_comment(value, **kwargs):
    is_brand_post = int(kwargs['data']['author_social_id']) == int(kwargs['data']['comment_author_id'])
    if is_brand_post:
        return InstaPostChannelType.BRAND.value
    return InstaPostChannelType.PUBLIC.value


def comment_url_creator(value, **kwargs):
    # Assuming the necessary variables are defined
    comment_id = kwargs['data'].get('comment_id', '')
    post_url = kwargs['data'].get('parent_post_url', '')
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
    main_data = kwargs.get("data")
    # if main_data:
    #     thumb_url = main_data.get("thumbnail_url", "")
    #     media_url = main_data.get("permalink", "")
    #     media_type = get_media_type(main_data.get('media_type'))
    #     return f"""<Attachments><Item><Name>{main_data.get('media_type')}</Name><MediaType>{media_type}</MediaType><ThumbUrl>{thumb_url}</ThumbUrl><Url>{media_url}</Url></Item></<Attachments>"""
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
    if int(setting_author_id) == int(kwargs['data']['comment_author_id']):
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
        "keys": ["comment_id"],
        "default_value": None,
        "handler_function": None,
        "clickhouse_column_name": "tweetidorfbid",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.PostSocialID": {
        "keys": ["post_social_id"],
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
        "keys": [],
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
        "keys": ["AttachmentXML"],
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
        "keys": ["media_type"],
        "default_value": "",
        "handler_function": handle_post_type_for_comment,
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
        "keys": ["comment_username"],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.AuthorName": {
        "keys": ["comment_username"],
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
        "keys": ["comment_author_id"],
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
