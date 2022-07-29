import os

from linebot import (
 WebhookHandler
)
testHandler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
