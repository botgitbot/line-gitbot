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



from utils.firebaseUtils import setDatabaseFromFirebase, setFirebaseFromDatabase


#    CREATE FLASK APP
app = Flask(__name__)

# SETUP LINE HANDLER
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


#    FLASK FUNCTION

@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'
