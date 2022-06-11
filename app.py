from flask import Flask, request, abort

from linebot import (
 WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage,
)





from eventBasedFunctions import replyBasedOnMessage
from routineFunctions import checkAndSendMessageIfEventHappensInAllRepo

from globalVariable import (
    interlude,
    port
)

#    CREATE FLASK


app = Flask(__name__)

#   GLOBAL VARIABLE


handler = WebhookHandler('f85e13929825bf9df787c225af107155')

#    FLASK FUNCTION


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
    # 'strip down' event, to get only the data we need
    msg_from_user = event.message.text
    followers_id = event.source.user_id
    reply_token = event.reply_token

    # call evenbased function
    replyBasedOnMessage(msg_from_user, followers_id, reply_token)



#   FUNCTION TO RUN EVERY MINUTE

import atexit
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

scheduler.add_job(func=checkAndSendMessageIfEventHappensInAllRepo, trigger="interval", seconds = interlude)

scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

#    RUN FLASK APP


import os
if __name__ == "__main__":
    portObject = int(os.environ.get('PORT', port))
    app.run(host='0.0.0.0', port=portObject)