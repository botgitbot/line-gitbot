from dotenv import load_dotenv
load_dotenv()
# now you can use value from .env with from `os.environ` or `os.getenv`

from handleGithubEvent.githubEventRouter import githubEventRouter
from utils.lineUtils import sendStringToGroup

from utils.utils import decryptGroupId, getPayload

from handleLineEvent.lineEventRouter import lineEventRouter


# IMPORT KAMUS(env, config, globalvariable)
import config 
import globalVariable
globalVariable.initialize()

# IMPORT SUBPROGRAM
from flask import Flask, request, abort
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



from utils.firebaseUtils import setDatabaseFromFirebase, setFirebaseFromDatabase


#    CREATE FLASK APP
app = Flask(__name__)

# SETUP LINE HANDLER
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# SETUP DATABASE
# when the app is first run, the database should be matching what's on firebase
setDatabaseFromFirebase()
print("database sekarang")
print(globalVariable.database)
#    FLASK FUNCTION

@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'


    

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



@app.route("/webhook/<token>", methods=['POST'])
def webhook(token):
    # decrypt path args buat dapetin group id
    group_id = decryptGroupId(token)
    # cek group id ada ngga di database bagian active. kalo ada, handle eventnya. kalo gada, do nothing(artinya gada group id tersebut yg nge invite kita)
    if(group_id in globalVariable.database["active"].keys()):
        #dapetin payload pake getPayload di util
        # send message ke group id tersebut
        payload = getPayload(request)
        # handle eventnya dengan cara lempar ke githubEventRouter. 
        githubEventRouter(payload, group_id)
    else:
        pass
    return 'OK'

# handle message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    lineEventRouter("message",event)
    # pake lineEventRouter
    pass


# handle leave group event
@handler.add(LeaveEvent)
def handle_leave(event):
    print("ada yg ngekick dari group!")
    lineEventRouter("leave", event)
    # pake handleGroupLeave
    pass
# handle diinvite ke dalem group
@handler.add(JoinEvent)
def handle_invite(event):
    print("join?")
    lineEventRouter("join", event)
    # pake handleGroupInvite

    pass


#    RUN FLASK APP
import os
if __name__ == "__main__":
    portObject = int(os.environ.get('PORT', config.PORT))
    app.run(host='0.0.0.0', port=portObject)