# IMPORT KAMUS(env, config, globalvariable)
from dotenv import load_dotenv
load_dotenv()
# # now you can use value from .env with from `os.environ` or `os.getenv`
import config 
# import globalVariable
# globalVariable.initialize()


# # IMPORT SUBPROGRAM
from flask import Flask, request, abort
import os
# from linebot import (
#  WebhookHandler
# )
# from linebot.exceptions import (
#     InvalidSignatureError
# )
# from linebot.models import (
#     MessageEvent,
#     TextMessage,
# )

# from eventBasedFunctions import replyBasedOnMessage
# from routineFunctions import checkAndSendMessageIfEventHappensInAllRepo


# from firebaseUtils import setDatabaseFromFirebase


#    CREATE FLASK APP
app = Flask(__name__)

# SETUP LINE HANDLER
# handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# SETUP DATABASE
# when the app is first run, the database should be matching what's on firebase
# setDatabaseFromFirebase()

#    FLASK FUNCTION

# /
@app.route('/')
def hello_world():
    return 'Hello World!' + os.getenv('TEST_ENV')




# ini route yang dipake saat pertama kali nge connect in ke line dev
# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#     return 'OK'

# # handle message
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     # 'strip down' event, to get only the data we need
#     msg_from_user = event.message.text
#     reply_token = event.reply_token
#     source_type = event.source.type
#     source_id = event.source.user_id
#     followers_id = event.source.user_id

#     if (source_type == 'user'):
#         source_id = event.source.user_id
#     elif (event.source.type == 'group'):
#         source_id = event.source.group_id

#     replyBasedOnMessage(msg_from_user, source_type, source_id, reply_token)


# #   FUNCTION TO RUN EVERY MINUTE
# import atexit
# from apscheduler.schedulers.background import BackgroundScheduler

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=checkAndSendMessageIfEventHappensInAllRepo, trigger="interval", seconds = config.INTERLUDE)
# scheduler.start()
# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())


#    RUN FLASK APP
import os
if __name__ == "__main__":
    portObject = int(os.environ.get('PORT', config.PORT))
    app.run(host='0.0.0.0', port=portObject)