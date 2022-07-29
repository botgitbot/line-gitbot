import json
import os
from dotenv import load_dotenv
load_dotenv()
# now you can use value from .env with from `os.environ` or `os.getenv`

from handleGithubEvent.githubEventRouter import githubEventRouter

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



from utils.firebaseUtils import setDatabaseFromFirebase


# SETUP LINE HANDLER
lineHandler = WebhookHandler('LINE_CHANNEL_SECRET')
# handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# SETUP DATABASE
# when the app is first run, the database should be matching what's on firebase
setDatabaseFromFirebase()
print("database sekarang")
print(globalVariable.database)

#    CREATE FLASK APP
app = Flask(__name__)



#    FLASK FUNCTION

@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!' +  json.dumps(globalVariable.database)


# ini route yang dipake saat pertama kali nge connect in ke line dev
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    print("request.headers")
    print(request.headers)
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        lineHandler.handle(body, signature)
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
        print(group_id)
        # handle eventnya dengan cara lempar ke githubEventRouter.
        print(payload.keys())
        githubEventRouter(payload, group_id)
    else:
        pass
    return 'OK'

@app.route('/<path:path>')
def catch_all(path):
    return Response("<h1>Flask</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")
# #    RUN FLASK APP
# import os
# if __name__ == "__main__":
#     portObject = int(os.environ.get('PORT', config.PORT))
#     app.run(host='0.0.0.0', port=portObject)