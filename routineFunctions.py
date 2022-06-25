import pytz
from datetime import datetime

import globalVariable
from lineUtils import sendStringToGroup
from utils import (
    fetchFromGithub,
    diffOfTimeLessThanEqualToInterlude
    )

def checkAndSendMessageIfEventHappensInAllRepo():
    group_id_arr = list(globalVariable.database.keys())
    for group_id in group_id_arr:
        repo_arr = list(globalVariable.database[group_id].keys())
        for usernameandrepo in repo_arr:
            print("usernameandrepo: " + usernameandrepo)
            access_token = globalVariable.database[group_id][usernameandrepo]["access_token"]
            usernameandrepo = usernameandrepo.replace("@", "/")

            #EVENT
            results = filterEventsToGetNewEventsOnly(usernameandrepo, access_token)
            if(len(results) != 0):
                print("ada event baru di", usernameandrepo)
                for event in results:
                    respondBasedOnEvent(usernameandrepo, event, group_id)
            else:
                print("tidak ada event baru di", usernameandrepo)


def respondBasedOnEvent(usernameandrepo, event, group_id):
    event_type = event["type"]
    if event_type == "PushEvent":
        respondOnPushEvent(usernameandrepo, event, group_id)

    elif event_type == "PullRequestEvent":
        respondOnPullRequestEvent(usernameandrepo, event, group_id)
    elif event_type == "ReleaseEvent" and event["payload"]["action"] == "published" and not(event["payload"]["prerelease"]):
        respondOnReleaseEvent(usernameandrepo, event, group_id)
    elif event_type == "PullRequestReviewCommentEvent":
        respondOnPullRequestReviewCommentEvent(usernameandrepo, event, group_id)
    # elif

def respondOnPushEvent(usernameandrepo, event, group_id):
    string_to_chat = f"[{usernameandrepo}] {event['actor']['login']} pushed to branch {event['payload']['ref']} with {event['payload']['size']} commits:"
    print(string_to_chat)
    for commit in event["payload"]["commits"]:
        string_to_chat += f"\n  - {commit['message']}"
    sendStringToGroup(group_id, string_to_chat)

def respondOnPullRequestEvent(usernameandrepo, event, group_id):
    string_to_chat = f"[{usernameandrepo}] {event['actor']['login']} {event['payload']['action']} pull request \"{event['payload']['pull_request']['title']}\" from {event['payload']['pull_request']['head']['ref']} to {event['payload']['pull_request']['base']['ref']}"
    print(string_to_chat)
    sendStringToGroup(group_id, string_to_chat)
    if event['actor']['login'] == "opened" and event['payload']['pull_request']['requested_reviewers']:
        string_to_chat += " with request to review from: "
        for reviewer in event['payload']['pull_request']['requested_reviewers']:
            string_to_chat += f"\n - {reviewer['login']} "
    print(string_to_chat)
    sendStringToGroup(group_id, string_to_chat)

def respondOnReleaseEvent(usernameandrepo, event, group_id):
    string_to_chat = f"[{usernameandrepo}] {event['actor']['login']} released tag {event['payload']['release']['tag_name']} \"{event['payload']['release']['name']}\""
    print(string_to_chat)
    sendStringToGroup(group_id, string_to_chat)

def respondOnPullRequestReviewCommentEvent(usernameandrepo, event, group_id):
    string_to_chat = f"[{usernameandrepo}] {event['actor']['login']} commented on pull request \"{event['payload']['pull_request']['title']}\""
    sendStringToGroup(group_id, string_to_chat)


def filterEventsToGetNewEventsOnly(usernameandrepo, access_token):
    # repo sama username buat ngeidentifikasi repo yang mana yang mo disentuh
    # return array of new event(new disini artinya event tersebut dilakukan selama interlude). kalo ga ada, return empty array
    
    # print("banyak event sampe saat ini:", len(res_dicts))
    start_time = datetime.now(pytz.utc).replace(tzinfo=None) 
    responds = fetchFromGithub(usernameandrepo, access_token)
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
