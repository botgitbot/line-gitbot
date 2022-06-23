# utils umum.
import requests
import json
from datetime import datetime

import config


def fetchPushEventFromGithub(usernameandrepo, access_token):
    url = 'https://api.github.com/repos/' + usernameandrepo +'/events'

    headers = {'Authorization': 'token ' + access_token}
    res_json = requests.get(url, headers=headers)
    res_dicts = json.loads(res_json.text)
    return res_dicts

def diffOfTimeLessThanEqualToInterlude(start_time, event_time_string):
    event_time = datetime.strptime(event_time_string, '%Y-%m-%dT%H:%M:%SZ')
    diff = start_time - event_time
    return diff.total_seconds() <= config.INTERLUDE