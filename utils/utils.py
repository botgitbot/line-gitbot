# utils umum.
import os
import json
from cryptography.fernet import Fernet
import base64

def sanitizeMessage(message):
    # sanitize msg_from_user
    # delete spaces in the back, and remove spaces that is more than one
    message = message.strip()
    message = ' '.join(message.split())
    return message

def splitMessageRepoUsernameToken(message):
    # message = "username/repo:token"
    # return "username", "repo", "token"
    repousername_token = message.split(":")
    repo_username = repousername_token[0]
    token = repousername_token[1]
    username = repo_username.split("/")[0]
    repo = repo_username.split("/")[1]
    return username, repo, token

def splitMessageRepoUsername(message):
    # message = "username/repo"
    # return "username", "repo"
    repousername = message.split("/")
    username = repousername[0]
    repo = repousername[1]
    return username, repo

def createDatabaseValueFromUsernameAndRepo(username, repo):
    return username + "@" + repo

def databaseValueToUsernameAndRepo(key):
    return key.split("@")[0], key.split("@")[1]


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