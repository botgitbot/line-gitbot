# general utils
import os
import json
from cryptography.fernet import Fernet
import base64
import globalVariable
from utils.firebaseUtils import setFirebaseFromDatabase
from config import placeholderWebhook

def sanitizeMessage(message):
    # sanitize msg_from_user
    # delete spaces in the back, and remove spaces that is more than one
    message = message.strip()
    message = ' '.join(message.split())
    return message


def encryptGroupId(groupid):
    # pake  PASSWORD_ENCRYPTION_KEY di env
    f = Fernet(os.getenv("PASSWORD_ENCRYPTION_KEY"))
    groupidAsByte = str.encode(groupid)
    tokenAsByte = f.encrypt(groupidAsByte)
    tokenAsStrWithBase32 = base64.b32encode(tokenAsByte).decode()
    return tokenAsStrWithBase32


def decryptGroupId(tokenAsStrWithBase32):
    # pake  PASSWORD_ENCRYPTION_KEY di env
    f = Fernet(os.getenv("PASSWORD_ENCRYPTION_KEY"))
    tokenAsByte = base64.b32decode(tokenAsStrWithBase32)
    groupIdAsByte = f.decrypt(tokenAsByte)
    groupIdAsStr = groupIdAsByte.decode()
    return groupIdAsStr


def getPayload(request):
    isForm = False
    try:
        if request.form['payload']:
            isForm = True
        isForm = True
    except:
        pass

    if isForm:
        inString = request.form['payload']
    else:
        inString = request.json
    # return dalam bentuk dict
    # instring to dict
    inDict = json.loads(inString)
    return inDict

def addWebhookToDatabase(group_id, username, repo):
    # add webhook to database
    urkey = usernameAndRepoAsDatabaseKey(username, repo)
    globalVariable.database["active"][group_id][urkey] = {"username": username, "repo": repo}
    setFirebaseFromDatabase()
    return

def isWebhookRecorded(group_id, username, repo):
    # check if webhook is recorded in database
    if(group_id in list(globalVariable.database["active"].keys())):
        urkey = usernameAndRepoAsDatabaseKey(username, repo)
        if(urkey in list(globalVariable.database["active"][group_id].keys())):
            return True
    return False


def usernameAndRepoAsDatabaseKey(username, repo):
    # username and repo to key
    return username + "@" + repo

def databaseKeyToUsernameAndRepo(key):
    # key to username and repo
    username = key.split("@")[0]
    repo = key.split("@")[1]
    return username, repo

def isGroupIdRecorded(group_id):
    # check if group_id is recorded in database
    if(group_id in list(globalVariable.database["active"].keys())):
        return True
    return False

def addGroupIdToActive(group_id):
    if(group_id in globalVariable.database["inactive"].keys()):
        globalVariable.database["active"][group_id] = globalVariable.database["inactive"][group_id]
        del globalVariable.database["inactive"][group_id]
    else:
        globalVariable.database["active"][group_id] = placeholderWebhook
    setFirebaseFromDatabase()