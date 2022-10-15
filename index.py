#LOAD ENV
from dotenv import load_dotenv

from utils.lineUtils import sendStringToGroup
load_dotenv(".env.dev")
# now you can use value from .env with from `os.environ` or `os.getenv`

from handleGithubEvent.githubEventRouter import githubEventRouter
from utils.utils import decryptGroupId, getPayload
from handleLineEvent.lineEventRouter import lineEventRouter


# IMPORT KAMUS(env, config, globalvariable)
import globalVariable
globalVariable.initialize()

# IMPORT SUBPROGRAM
from flask import Flask, request, abort, Response
import os
from linebot import (
 WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    LeaveEvent,
    JoinEvent,
    TextMessage,
)


from utils.firebaseUtils import setDatabaseFromFirebase

from config import placeholderWebhook

# SETUP LINE HANDLER
# lineHandler = WebhookHandler('LINE_CHANNEL_SECRET')
lineHandler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# EXCEPTION HANDLER
def handleException(e):
    # send error message to LINE Group
    sendStringToGroup("C05d96b6e4830bac9f4d10ee890c09666", "error = " + str(e))
    return "error"

# SETUP DATABASE
# when the app is first run, the database should be matching what's on firebase
setDatabaseFromFirebase()

#    CREATE FLASK APP
app = Flask(__name__)

#    FLASK FUNCTION

@app.route('/', methods=['GET'])
def hello():
    return os.getenv("DEPLOYMENT_MESSAGE")



# ini route yang dipake saat pertama kali nge connect in ke line dev
@app.route("/callback", methods=['POST'])
def callback():
    try:
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']
        # get request body as text
        body = request.get_data(as_text=True)
        # app.logger.info("Request body: " + body)
        # handle webhook body
        try:
            lineHandler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)
        return 'OK'
    except Exception as e:
        return handleException(e)

@app.route("/webhook/<token>", methods=['POST'])
def webhook(token):
    try:
        # decrypt path args buat dapetin group id
        group_id = decryptGroupId(token)
        # cek group id ada ngga di database bagian active. kalo ada, handle eventnya. kalo gada, do nothing(artinya gada group id tersebut yg nge invite kita)
        if(group_id in globalVariable.database["active"].keys()):
            #dapetin payload pake getPayload di util
            # send message ke group id tersebut
            payload = getPayload(request)
            # handle eventnya dengan cara lempar ke githubEventRouter.
            githubEventRouter(payload, group_id)

        return 'OK'
    except Exception as e:
        return handleException(e)

# handle message
@lineHandler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        lineEventRouter("message",event)
    except Exception as e:
        return handleException(e)

# handle leave group event
@lineHandler.add(LeaveEvent)
def handle_leave(event):
    try:
        lineEventRouter("leave", event)
    except Exception as e:
        return handleException(e)
# handle diinvite ke dalem group
@lineHandler.add(JoinEvent)
def handle_invite(event):
    try:
        lineEventRouter("join", event)
    except Exception as e:
        return handleException(e)
    
@app.route('/<path:path>')
def catch_all(path):
        
    return Response("<p>You visited: /%s</p>" % (path), mimetype="text/html")


# a way to check current variable state
@app.route("/testvariable", methods=['GET'])
def testVariable():
    try:
        # send current variable to LINE Group
        sendStringToGroup("C05d96b6e4830bac9f4d10ee890c09666", "testvariable")
        sendStringToGroup("C05d96b6e4830bac9f4d10ee890c09666", "globalVariable = " + str(globalVariable.database))
        sendStringToGroup("C05d96b6e4830bac9f4d10ee890c09666", "placeholderWebhook = " +  str(placeholderWebhook))
        return "test"
    except Exception as e:
        return handleException(e)

# #    RUN FLASK APP
import config 
if __name__ == "__main__":
    portObject = int(os.environ.get('PORT', config.PORT))
    app.run(host='0.0.0.0', port=portObject)



