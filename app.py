'''
    IMPORT
'''
from cmath import e
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


import atexit
from apscheduler.schedulers.background import BackgroundScheduler


from eventBasedFunctions import replyBasedOnMessage
from routineFunctions import checkNewEventInRepos

from globalVariable import database
'''
    CREATE FLASK
'''

app = Flask(__name__)

'''
    GLOBAL VARIABLE
'''

handler = WebhookHandler('f85e13929825bf9df787c225af107155')
interlude = 10

followersData = {}
    # "U195dcbc6b51ab6056d2f9a9c5dfde093":
    #     {"repos": ["test-line-bot"], "username": "addinnabilal", "access_token": "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"}},

'''
    FLASK FUNCTION
'''

# ini route yang dipake saat pertama kali nge connect in ke line dev
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
    global repo
    global username
    global access_token

    # ALGORITHM
    
    # get message yang diketikin sama user. simpen ke dalem variable msg_from_user
    msg_from_user = event.message.text
    followers_id = event.source.user_id

    # do something dengan bergantung sama messsage yang di chat sama user.

    # panggil evenbased function
    replyBasedOnMessage(msg_from_user, followers_id)


'''
    HELPER FUNCTION
'''


'''
    FUNCTION TO RUN EVERY MINUTE
'''


scheduler = BackgroundScheduler()

scheduler.add_job(func=checkNewEventInRepos, trigger="interval", seconds = interlude)

scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

'''
    RUN FLASK APP
'''

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)