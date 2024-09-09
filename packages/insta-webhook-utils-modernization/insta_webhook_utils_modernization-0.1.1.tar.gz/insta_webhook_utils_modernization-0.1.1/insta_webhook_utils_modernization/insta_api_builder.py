import httpx
import asyncio
import logging
from typing import Optional, Dict, Any

# Set up logging for error handling
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstagramAPI:
    _instance = None

    def __new__(cls, base_url: str, api_version: str):
        if cls._instance is None:
            cls._instance = super(InstagramAPI, cls).__new__(cls)
            cls._instance.base_url = base_url
            cls._instance.api_version = api_version
        return cls._instance

    async def make_get_request(self, endpoint: str, params: Dict[str, str]) -> Optional[str]:
        """Helper method to make asynchronous GET requests with error handling and rate limit support."""
        url = f"{self.base_url}/{self.api_version}/{endpoint}"
        retry_attempts = 5  # Max retries in case of rate-limiting
        for attempt in range(retry_attempts):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)

                    # Handle Rate Limiting (Error 429)
                    if response.status_code == httpx.codes.TOO_MANY_REQUESTS:
                        rate_limit_reset = response.headers.get('X-RateLimit-Reset')
                        if rate_limit_reset:
                            wait_time = int(rate_limit_reset) - int(response.headers.get('X-Timestamp', 0))
                            logger.warning(f"Rate limit hit. Waiting for {wait_time} seconds to reset.")
                            await asyncio.sleep(wait_time)
                        else:
                            wait_time = 2 ** attempt  # Exponential backoff
                            logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds.")
                            await asyncio.sleep(wait_time)
                        continue  # Retry request after waiting

                    # Handle other errors
                    if response.status_code != httpx.codes.OK:
                        logger.error(f"Error {response.status_code}: {response.text}")
                        self.log_error(url, params, response)
                        return None

                    return response.text

            except httpx.RequestError as http_err:
                logger.error(f"HTTP request error on attempt {attempt + 1}: {http_err}")
                if attempt < retry_attempts - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error("Max retries reached. Cannot recover from the error.")
                    self.log_error(url, params, http_err)
                    return None
            except Exception as ex:
                logger.error(f"Unexpected error: {ex}")
                self.log_error(url, params, ex)
                return None

        return None

    async def fetch_instagram_data(
            self,
            endpoint: str,
            access_token: str,
            fields: str,
            extra_params: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        """Generic method to fetch Instagram data using a dynamic endpoint and fields."""
        params = {
            "access_token": access_token,
            "fields": fields
        }
        if extra_params:
            params.update(extra_params)

        return await self.make_get_request(endpoint, params)

    @staticmethod
    def log_error(url: str, params: Dict[str, str], error: Any) -> None:
        """Log errors for debugging."""
        error_details = {
            "URL": url,
            "Parameters": params,
            "Error": str(error)
        }
        logger.error(f"Error Details: {error_details}")


def extract_single_id(data):
    """
    Recursively extract the first 'id' field from the Instagram webhook JSON data.

    :param data: JSON data (dict or list) to search for 'id' field.
    :return: The first 'id' value found in the JSON, or None if no 'id' field is found.
    """
    # If the data is a dictionary
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'id':
                return value  # Return the first 'id' value found
            elif isinstance(value, (dict, list)):
                result = extract_single_id(value)  # Recursively search within nested structures
                if result:
                    return result

    # If the data is a list
    elif isinstance(data, list):
        for item in data:
            result = extract_single_id(item)  # Recursively search each item
            if result:
                return result


# Example usage with async calls
async def main():
    # Initialize with base URL and API version at runtime
    api = InstagramAPI(base_url="https://graph.facebook.com", api_version="v12.0")

    access_token = "your_access_token"
    media_id = "your_media_id"

    # Fetch media data dynamically
    media_data = await api.fetch_instagram_data(
        endpoint=media_id,
        access_token=access_token,
        fields="id,caption,media_type,media_url,permalink,thumbnail_url,timestamp"
    )
    print("Media Data:", media_data)

    # Fetch comments data dynamically
    comments_data = await api.fetch_instagram_data(
        endpoint=f"{media_id}/comments",
        access_token=access_token,
        fields="id,text,username,timestamp"
    )
    print("Comments Data:", comments_data)


if __name__ == "__main__":
    asyncio.run(main())
