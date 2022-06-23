# utils umum.
import requests
import json
from datetime import datetime

import config


def fetchFromGithub(usernameandrepo, access_token):
    url = 'https://api.github.com/repos/' + usernameandrepo +'/events'
    headers = {'Authorization': 'token ' + access_token}
    res_json = requests.get(url, headers=headers)
    res_dicts = json.loads(res_json.text)
    return res_dicts

def diffOfTimeLessThanEqualToInterlude(start_time, event_time_string):
    event_time = datetime.strptime(event_time_string, '%Y-%m-%dT%H:%M:%SZ')
    diff = start_time - event_time
    print("beda waktu", end=": ")
    print(diff.total_seconds())
    return diff.total_seconds() <= config.INTERLUDE

def checkIfRepoAndAccessTokenValid(usernameandrepo, access_token):
    if (usernameandrepo == '' or access_token == ''):
        return False
    url = 'https://api.github.com/repos/' + usernameandrepo +'/events'
    headers = {'Authorization': 'token ' + access_token}
    res_json = requests.get(url, headers=headers)
    if (res_json.status_code == 200):
        return True
    return False
    