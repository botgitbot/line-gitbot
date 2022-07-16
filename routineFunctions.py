from responds.respondOnPullRequestReviewCommentEvent import respondOnPullRequestReviewCommentEvent

import globalVariable
from utils.lineUtils import sendStringToGroup
from responds.respondOnPullRequestEvent import respondOnPullRequestEvent
from responds.respondOnPushEvent import respondOnPushEvent
from responds.respondOnReleaseEvent import respondOnReleaseEvent
from utils.utils import (
    filterEventsToGetNewEventsOnly,
    keyToUsernameAndRepo
    )

def checkAndSendMessageIfEventHappensInAllRepo():
    group_id_arr = list(globalVariable.database.keys())
    for group_id in group_id_arr:
        repo_arr = list(globalVariable.database[group_id].keys())
        for key in repo_arr:
            # print("key: " +key)
            access_token = globalVariable.database[group_id][key]["access_token"]


            #EVENT
            username, repo = keyToUsernameAndRepo(key)
            results = filterEventsToGetNewEventsOnly(username, repo, access_token)
            if(len(results) != 0):
                print("ada event baru di", username + "/" + repo)
                for event in results:
                    respondBasedOnEvent(username, repo, event, group_id)
            else:
                pass
                # print("tidak ada event baru di", username + "/" + repo)


def respondBasedOnEvent(username, repo, event, group_id):
    event_type = event["type"]
    if event_type == "PushEvent":
        respondOnPushEvent(username, repo , event, group_id)

    elif event_type == "PullRequestEvent":
        respondOnPullRequestEvent(username, repo, event, group_id)
    elif event_type == "ReleaseEvent" and event["payload"]["action"] == "published" and not(event["payload"]["release"]["prerelease"]):
        respondOnReleaseEvent(username, repo, event, group_id)
    elif event_type == "PullRequestReviewCommentEvent":
        respondOnPullRequestReviewCommentEvent(username, repo, event, group_id)