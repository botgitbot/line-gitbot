# semua interface yang make module line
# fungsi lain gada yang nyentuh line_bot_api
from globalVariable import database
import os

from linebot import (
    LineBotApi
)
from linebot.models import (
    TextSendMessage,
)

from globalVariable import config

line_bot_api = LineBotApi(config['LINE_CHANNEL_ACCESS_TOKEN'])
# awalnya fungsi dibawah namanya 'chatToFollower'. aku ganti jadi sendString biar 1. lebih explisit(yang aku kirim string. keknya bisa selain string deh, dan kalo pake kata chat, terlalu luas jdinya) 2. bisa bedain antara 'send langsung sama reply'(karena keduanya termasuk chat)

# mungkin next stepnya, buat ningkatin abstraksi, bisa dibikin fungsi chat() yang palugada, all in one.
def sendStringToFollower(follower_id, string_to_send):
    line_bot_api.push_message(follower_id, TextSendMessage(text=string_to_send))

def replyString(reply_token, string_to_send):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=string_to_send))