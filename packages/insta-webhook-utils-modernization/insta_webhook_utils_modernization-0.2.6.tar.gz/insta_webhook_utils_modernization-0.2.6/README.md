# Basic helper classes for Instagram Webhook

This code provides the common code for the instagram webhook classes that are required for the modification of the data at different services
## Installation

Install the package using pip:

```sh
pip install insta-webhook-utils-modernization
```
# Usage
## Basic Usage
To identify the event type received from the webhook use the following function, it returns the Enum 
```python
from insta_webhook_utils_modernization.indentifier_code import classify_instagram_event, InstagramEventType

event_type: InstagramEventType = classify_instagram_event(event dict|str)

```
