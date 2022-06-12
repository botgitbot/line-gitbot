import pytz
from datetime import datetime

from globalVariable import database
from lineUtils import sendStringToFollower
from utils import (
    fetchFromGithub,
    diffOfTimeLessThanEqualToInterlude
    )

def checkAndSendMessageIfEventHappensInAllRepo():
    follower_id_arr = list(database.keys())
    for follower_id in follower_id_arr:
        print("follower id: " + follower_id)
        print("username: " + database[follower_id]["username"])
        print("access token: " + database[follower_id]["access_token"])
        for repo in database[follower_id]["repos"]:
            print("repo: " + repo)
            results = filterEventsToGetNewEventsOnly(repo, database[follower_id]["username"], database[follower_id]["access_token"])
            if(len(results) != 0):
                print("ada event baru")
                for result in results:
                    if result["type"] == "PushEvent":
                        # {result["actor"]["login"]} pushed to branch {result["payload"]["ref"]} {result["payload"]["commits"][0]["url"]}
                        string_to_chat = f"[{repo}] {result['actor']['login']} pushed to branch {result['payload']['ref']} with {result['payload']['size']} commits:"
                        print(string_to_chat)
                        for commit in result["payload"]["commits"]:
                            string_to_chat += f"\n  - {commit['message']}"
                        sendStringToFollower(follower_id, string_to_chat)
            else:
                print("tidak ada event baru")
                # chatToFollower(follower_id, "tidak ada event baru")


def filterEventsToGetNewEventsOnly(repo, username, access_token):
    # repo sama username buat ngeidentifikasi repo yang mana yang mo disentuh
    # return array of new event(new disini artinya event tersebut dilakukan selama interlude). kalo ga ada, return empty array
    
    # print("banyak event sampe saat ini:", len(res_dicts))
    start_time = datetime.now(pytz.utc).replace(tzinfo=None) 
    responds = fetchFromGithub(username+"/"+repo, access_token)
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
