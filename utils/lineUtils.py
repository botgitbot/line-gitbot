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

# print(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
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