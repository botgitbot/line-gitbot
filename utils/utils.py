# utils umum.
import pytz
import requests
import json
from datetime import datetime

import config


def fetchFromGithub(username, repo , access_token):
    return fetchEventFromGithub(username, repo, access_token)

def fetchEventFromGithub(username, repo, access_token):

    url = 'https://api.github.com/repos/' + username + "/" + repo +'/events'
    # print(url)
    headers = {'Authorization': 'token ' + access_token}
    res_json = requests.get(url, headers=headers)
    res_dicts = json.loads(res_json.text)
    return res_dicts

def diffOfTimeLessThanEqualToInterlude(start_time, event_time_string):
    event_time = datetime.strptime(event_time_string, '%Y-%m-%dT%H:%M:%SZ')
    diff = start_time - event_time


    # print recent
    if(diff.total_seconds() <= 9*config.INTERLUDE):
        print("beda waktu", end=": ")
        print(diff.total_seconds())


    
    return diff.total_seconds() <= (config.INTERLUDE + config.TIME_TOLERANCE)

def checkIfRepoAndAccessTokenValid(usernameandrepo, access_token):
    if (usernameandrepo == '' or access_token == ''):
        return False
    url = 'https://api.github.com/repos/' + usernameandrepo +'/events'
    headers = {'Authorization': 'token ' + access_token}
    res_json = requests.get(url, headers=headers)
    if (res_json.status_code == 200):
        return True
    return False
    
def filterEventsToGetNewEventsOnly(username, repo, access_token):
    # repo sama username buat ngeidentifikasi repo yang mana yang mo disentuh
    # return array of new event(new disini artinya event tersebut dilakukan selama interlude). kalo ga ada, return empty array
    
    # print("banyak event sampe saat ini:", len(res_dicts))
    start_time = datetime.now(pytz.utc).replace(tzinfo=None) 
    responds = fetchFromGithub(username, repo, access_token)
    # print("waktu sekarang", start_time)
    # iterasi setiap response, jika ada response yang dibuat < 5 menit terakhir, add to results
    results = []
    for res in responds:        
        # "2022-05-25T05:58:32Z"
        event_time_string = res["created_at"]

        if(diffOfTimeLessThanEqualToInterlude(start_time, event_time_string)):
            print("ada event baru!")
            results.append(res)
    return results

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

def createKeyFromUsernameAndRepo(username, repo):
    return username + "@" + repo

def keyToUsernameAndRepo(key):
    return key.split("@")[0], key.split("@")[1]