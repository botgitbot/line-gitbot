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

import requests

'''
    CREATE FLASK
'''

app = Flask(__name__)

'''
    GLOBAL VARIABLE
'''

line_bot_api = LineBotApi('hBs3vE924/xltPVsO3ef+5Jz0Fn7nCUS7LiDlaoI9C89tMv0oha23N/BpyV4yrKmCtdP0VuBTPNuXTLjse7yGNdqSdb9+iOk9M0SHfZOhLzbcdQzB/LP4oDiEVxKz6BOp0X+lZ2noXKdwvY/Pj44BwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f85e13929825bf9df787c225af107155')

repo = ""
username = ""

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



# handle message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # KAMUS
    global var
    global arrOfNumber
    global repo
    global username

    # ALGORITHM
    
    # get message yang diketikin sama user. simpen ke dalem variable msg_from_user
    msg_from_user = event.message.text
    
    # do something dengan bergantung sama messsage yang di chat sama user.
    if msg_from_user=="test": # memastikan flask berjalan dengan aman
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="coba github api!"))

    elif msg_from_user[0] == "!" and msg_from_user[1] == "r": # catet repo 
        # karakter selanjutnya adalah reponya
        repo = msg_from_user[2:]
        message = TextSendMessage(text = "repo:"+ repo)
        line_bot_api.reply_message(event.reply_token, message)
    
    elif msg_from_user[0] == "!" and msg_from_user[1] == "u": # catet username
        # karakter selanjutnya adalah username
        username = msg_from_user[2:]
        message = TextSendMessage(text = "username: " + username)
        line_bot_api.reply_message(event.reply_token, message)
    elif msg_from_user == "getcommit":
        url = 'https://api.github.com/repos/' + username + '/' + repo + '/commits'
        print("url: " + url)
        response = requests.get(url)
        print("response:", response)
        string_to_send = "ada " + len(response) + " jumlah commit di repo " + repo + "!"
        message = TextSendMessage(text=string_to_send)
        line_bot_api.reply_message(event.reply_token, message)
    else: 
        message = TextSendMessage(text="bukan command khusus!")
        line_bot_api.reply_message(event.reply_token, message)


'''
    HELPER FUNCTION
'''

def getNewCommit(repo_id):
    # repo_id is identifier buat 'repo yang mana'
    # return array of new commit. kalo ga ada, return empty array
    pass


'''
    RUN FLASK APP
'''

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)




'''
    FUNCTION TO RUN EVERY MINUTE
'''

# import time
# import atexit

# from apscheduler.schedulers.background import BackgroundScheduler


# def print_date_time():
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


# scheduler = BackgroundScheduler()
# scheduler.add_job(func=print_date_time, trigger="interval", seconds=60)
# scheduler.start()

# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())