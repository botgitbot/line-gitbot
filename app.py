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

    # ALGORITHM
    
    # get message yang diketikin sama user. simpen ke dalem variable msg_from_user
    msg_from_user = event.message.text
    
    # do something dengan bergantung sama messsage yang di chat sama user.
    if msg_from_user=="test": # memastikan flask berjalan dengan aman
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="flask app is running!"))

    elif msg_from_user == "followers":
        followers = line_bot_api.get_followers_ids()
        print("followers: " + str(followers))
        message = TextSendMessage(text = "followers is printed in console")
        line_bot_api.reply_message(event.reply_token, message)

    elif msg_from_user == "eventinfo":
        print("eventinfo: " + str(event))
        message = TextSendMessage(text = "event is printed in console")
        line_bot_api.reply_message(event.reply_token, message)


    elif msg_from_user == "printarray":
        message = TextSendMessage(text = "array of number = " + str(["1","2","3","4","5"]))
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
    port = int(os.environ.get('PORT', 5000))
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