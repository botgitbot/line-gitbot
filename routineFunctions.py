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
            results = filterEventsToGetNewEventsOnly(usernameandrepo.replace("@", "/"), access_token)
            if(len(results) != 0):
                print("ada event baru di", usernameandrepo)
                for result in results:
                    if result["type"] == "PushEvent":
                        string_to_chat = f"[{usernameandrepo}] {result['actor']['login']} pushed to branch {result['payload']['ref']} with {result['payload']['size']} commits:"
                        print(string_to_chat)
                        for commit in result["payload"]["commits"]:
                            string_to_chat += f"\n  - {commit['message']}"
                        sendStringToGroup(group_id, string_to_chat)
            else:
                print("tidak ada event baru di", usernameandrepo)
                # chatTogroup(group_id, "tidak ada event baru")


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
