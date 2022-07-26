# semua interface yang make module line
# fungsi lain gada yang nyentuh line_bot_api
import os

from linebot import (
    LineBotApi
)
from linebot.models import (
    TextSendMessage,
    FlexSendMessage
)

# from globalVariable import config

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
# awalnya fungsi dibawah namanya 'chatToFollower'. aku ganti jadi sendString biar 1. lebih explisit(yang aku kirim string. keknya bisa selain string deh, dan kalo pake kata chat, terlalu luas jdinya) 2. bisa bedain antara 'send langsung sama reply'(karena keduanya termasuk chat)

# mungkin next stepnya, buat ningkatin abstraksi, bisa dibikin fungsi chat() yang palugada, all in one.
def sendStringToGroup(group_id, string_to_send):
    line_bot_api.push_message(group_id, TextSendMessage(text=string_to_send))

def sendFlexMessageToGroup(group_id, flex_message):
    line_bot_api.push_message(group_id, FlexSendMessage(alt_text="Flex Message", contents=flex_message))
    
def replyString(reply_token, string_to_send):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=string_to_send))

def replyFlexMessage(reply_token, flex_message):
    line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text="Flex Message", contents=flex_message))

def replyFlexMessageTemplateTitleText(reply_token, title, text_content):
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "color": "#576F72",
                "size": "14px"
            },
            {
                "type": "text",
                "text": text_content,
                "wrap": True,
                "size": "14px"
            }
            ],
            "backgroundColor": "#F0EBE3",
            "paddingAll": "30px"
        },
        "size": "kilo"
    }
    replyFlexMessage(reply_token, flex_message)

def pushFlexMessageTemplateTitleTextToGroup(group_id, title, text_content):
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "color": "#576F72",
                "size": "14px"
            },
            {
                "type": "text",
                "text": text_content,
                "wrap": True,
                "size": "14px"
            }
            ],
            "backgroundColor": "#F0EBE3",
            "paddingAll": "30px"
        },
        "size": "kilo"
    }
    sendFlexMessageToGroup(group_id, flex_message)

def replyFlexMessageTemplateTitleTextUrl(reply_token, title, text_content, uri):
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "color": "#576F72",
                "size": "14px"
            },
            {
                "type": "text",
                "text": text_content,
                "wrap": True,
                "size": "14px"
            },
            {
                "type": "button",
                "action": {
                "type": "uri",
                "label": "Click me",
                "uri": uri
                },
                "style": "link",
                "color": "#576F72"
            }
            ],
            "backgroundColor": "#F0EBE3",
            "paddingAll": "30px"
        },
        "size": "kilo"
    }
    replyFlexMessage(reply_token, flex_message)

def pushFlexMessageTemplateTitleTextUrlToGroup(group_id, title, text_content, uri):
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "color": "#576F72",
                "size": "14px"
            },
            {
                "type": "text",
                "text": text_content,
                "wrap": True,
                "size": "14px"
            },
            {
                "type": "button",
                "action": {
                "type": "uri",
                "label": "Click me",
                "uri": uri
                },
                "style": "link",
                "color": "#576F72"
            }
            ],
            "backgroundColor": "#F0EBE3",
            "paddingAll": "30px"
        },
        "size": "kilo"
    }
    sendFlexMessageToGroup(group_id, flex_message)



class standardFlexMessageClass:
    def __init__(self, title, text_content):
        self.flexMessageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "color": "#576F72",
                "size": "14px"
            },
            {
                "type": "text",
                "text": text_content,
                "wrap": True,
                "size": "14px"
            }
            ],
            "backgroundColor": "#F0EBE3",
            "paddingAll": "30px"
        },
        "size": "kilo"
    }

class flexMessageWithUrlClass:
    def __init__(self, title, text_content, url, button_text):
        self.flexMessageTemplate = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "color": "#576F72",
                "size": "14px"
            },
            {
                "type": "text",
                "text": text_content,
                "wrap": True,
                "size": "14px"
            },
            {
                "type": "button",
                "action": {
                    "type": "uri",
                    "label": button_text,
                    "uri": url
                },
                "style": "primary",
                "color": "#576F72",
                "margin": "5px",
                "height": "sm"
                }
            ],
            "backgroundColor": "#F0EBE3",
            "paddingAll": "30px"
        },
        "size": "kilo"
    }