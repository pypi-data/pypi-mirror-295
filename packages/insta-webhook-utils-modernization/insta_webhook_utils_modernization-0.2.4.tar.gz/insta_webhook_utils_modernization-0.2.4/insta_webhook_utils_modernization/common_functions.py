import json
from datetime import datetime
from typing import Tuple, List, Dict, Optional


def get_media_type(media_type: str) -> int:
    media_type = (media_type or "").upper()

    media_type_mapping = {
        "": 1,
        "TEXT": 1,
        "TXT": 1,
        "STATUS": 1,
        "POSTBACK": 1,
        "CONVERSATION": 1,
        "PHOTO": 2,
        "IMAGE": 2,
        "ALBUM": 2,
        "CAROUSEL": 2,
        "IMAGE/JPEG": 2,
        "IMAGE/PNG": 2,
        "CAROUSEL_ALBUM": 2,
        "STICKER": 2,
        "VIDEO/MP4": 3,
        "VIDEO_INLINE": 3,
        "VIDEO - CHECKIN": 3,
        "VIDEO-CHECKIN": 3,
        "ADDED_VIDEO": 3,
        "VIDEO": 3,
        "ARTICLE": 4,
        "URL": 4,
        "LINK": 4,
        "POLL": 5,
        "VISUAL_POLL": 5,
        "ANIMATEDGIF": 7,
        "ANIMATED_IMAGE_SHARE": 7,
        "ANIMATED_IMAGE_AUTOPLAY": 7,
        "ANIMATED_GIF": 7,
        "ANIMATED_IMAGE_VIDEO_AUTOPLAY": 7,
        "ANIMATED_IMAGE_VIDEO": 7,
        "IMAGE/GIF": 7,
        "DOC": 9,
        "DOCX": 9,
        "APPLICATION/MSWORD": 9,
        "PDF": 8,
        "APPLICATION/PDF": 8,
        "EXCEL": 10,
        "XLSX": 10,
        "AUDIO": 11,
        "VOICE": 11,
        "CONTACTS": 12,
        "CONTACT": 12,
        "SYSTEM": 13,
        "LOCATION": 14,
        "LOCATIONS": 14,
        "HTML": 15,
        "CARD": 16,
        "QUICKREPLY": 17,
        "BUTTONS": 18,
        "BUTTON": 18,
        "FILE": 19,
        "TEMPLATE": 20,
        "REELS": 21
    }
    # Return the value if found, otherwise default to 6
    return media_type_mapping.get(media_type, 6)


async def extracting_parent_post(clickhouse_obj, parent_post_id: str, category_ids, brand_ids,
                                 channel_group_id: int) -> Optional[dict]:
    clickhouse_query = f"""
        SELECT tagid, tweetidorfbid, channeltype, channelgroupid,instagramgraphapiid,isbrandpost,url, posttype, mediaenum, mediatype 
        FROM spatialrss.mentiondetails  final
        PREWHERE categoryid IN ({category_ids}) AND brandid IN ({brand_ids}) 
        WHERE channelgroupid={channel_group_id} AND tweetidorfbid='{parent_post_id}'
    """
    clickhouse_obj.execute(clickhouse_query)
    df = clickhouse_obj.fetch_df()
    return None


def extract_brand_ids_and_category_ids(data: List[Dict]) -> Tuple[str, str]:
    # Extract Brand IDs and Category IDs
    brand_ids = ",".join(str(item['BrandID']) for item in data)
    category_ids = ",".join(str(item['CategoryID']) for item in data)
    return brand_ids, category_ids


async def process_parent_post(post_id, instagram_api, access_token):
    response_data = await instagram_api.fetch_instagram_data(
        endpoint=post_id,
        access_token=access_token,
        fields="permalink,id,caption,comments_count,like_count,media_type,media_url,owner{name,username,ig_id,id,followers_count,follows_count,media_count,biography,profile_picture_url,website},ig_id,username,shortcode,thumbnail_url,media_product_type,is_comment_enabled,timestamp,children{media_type,media_url,thumbnail_url}"
        # TODO: get this from setting
    )
    if response_data and isinstance(response_data, str):
        response_data = json.loads(response_data)

    return response_data


def extracting_common_details(setting_obj, channel_type, instagram_channel_group_id):
    current_time = datetime.utcnow()
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S')
    return {
        "in_time": formatted_time,
        "channel_group_id": instagram_channel_group_id,
        "channel_type": channel_type,
        "category_id": setting_obj.get("CategoryID"),
        "category_name": setting_obj.get("CategoryName"),
        "brand_id": setting_obj.get("BrandID"),
        "brand_name": setting_obj.get("BrandName"),
        "setting_id": setting_obj.get("AccountID"),
        "author_social_id": setting_obj.get("InstagramGraphApiID"),
        "user_profile_pic": setting_obj.get("ProfilePic")
    }
