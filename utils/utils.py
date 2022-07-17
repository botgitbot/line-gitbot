# utils umum.
import pytz
import requests
import json
from datetime import datetime

import config


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
    return  groupid

def decryptGroupId(groupid):
    # pake  PASSWORD_ENCRYPTION_KEY di env
    return  groupid


def getPayload(request):
    isForm = False
    try:
        if request.form['payload']:
            isForm = True
        isForm = True
        print("keknya form")
    except:
        print("keknya json")
        pass

    if isForm:
        print("payload(form)")
        print(type(request.form))
        print(request.form.keys())
        # dict_keys(['payload'])
        print(request.form['payload'])
        inString = request.form['payload']
    else:
        print("payload(json)")
        print(request.json)
        inString = request.json
    # return dalam bentuk dict
    return {}