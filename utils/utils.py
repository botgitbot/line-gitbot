# utils umum.
import os
import json
from cryptography.fernet import Fernet
import base64
import globalVariable
from utils.firebaseUtils import setFirebaseFromDatabase

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

def addWebhookToDatabase(group_id, hook_id, username, repo):
    # add webhook to database
    globalVariable.database["active"][group_id][hook_id] = {"username": username, "repo": repo}
    setFirebaseFromDatabase()
    return