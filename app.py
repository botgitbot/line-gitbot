'''
    IMPORT
'''
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


'''
    CREATE FLASK
'''

app = Flask(__name__)

'''
    GLOBAL VARIABLE
'''

line_bot_api = LineBotApi('hBs3vE924/xltPVsO3ef+5Jz0Fn7nCUS7LiDlaoI9C89tMv0oha23N/BpyV4yrKmCtdP0VuBTPNuXTLjse7yGNdqSdb9+iOk9M0SHfZOhLzbcdQzB/LP4oDiEVxKz6BOp0X+lZ2noXKdwvY/Pj44BwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f85e13929825bf9df787c225af107155')

var="default"

consolelog = ""


'''
    FLASK FUNCTION
'''

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # KAMUS
    global var
    global consolelog

    # ALGORITHM
    
    # get message yang diketikin sama user. simpen ke dalem variable msg_from_user
    msg_from_user = event.message.text
    
    # do something dengan bergantung sama messsage yang di chat sama user.
    if msg_from_user=="test": # memastikan flask berjalan dengan aman
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="flask app is running with event info and followers edited!"))
    elif msg_from_user=="tesvar": # test buat nyimpen variable
        message = TextSendMessage(text="var = " + var)
        line_bot_api.reply_message(event.reply_token, message)

    elif msg_from_user == "followers":
        followers = line_bot_api.get_followers_ids()

        string_to_send = ""
        string_to_send += "tipe dari followers adalah " + type(followers) + "\n"
        # string_to_send += "asumsi dia objek, atributnya adalah" + getattr(followers) + "\n"
        # string_to_send += "followers =  " + str(followers) + "\n"

        consolelog += string_to_send

        message = TextSendMessage(text = string_to_send)
        line_bot_api.reply_message(event.reply_token, message)

    elif msg_from_user == "eventinfo":
         
        string_to_send = ""
        string_to_send += "tipe dari event adalah " + type(event) + "\n"
        string_to_send += "asumsi dia objek, atributnya adalah" + getattr(event) + "\n"
        string_to_send += "event =  " + str(event) + "\n"

        consolelog += string_to_send

        message = TextSendMessage(text = string_to_send)
        line_bot_api.reply_message(event.reply_token, message)


    # FOR DEBUGGING PURPOSE
    elif msg_from_user == "debug":
        message = TextSendMessage(text = consolelog)
        line_bot_api.reply_message(event.reply_token, message)
    elif msg_from_user == "cleardebug":
        consolelog = ""
        message = TextSendMessage(text = "consolelog is cleared")
        line_bot_api.reply_message(event.reply_token, message)
    else: # kalau messagenya != "test", nyimpen text ke variable var
        var=msg_from_user
        message = TextSendMessage(text="berhasil menyimpan " + var + "!")
        line_bot_api.reply_message(event.reply_token, message)


'''
    HELPER FUNCTION
'''



'''
    RUN FLASK APP
'''

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
