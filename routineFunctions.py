import requests
import json
from datetime import datetime
import pytz


def checkNewEventInRepos():
    global followersData
    follower_id_arr = list(followersData.keys())
    for follower_id in follower_id_arr:
        print("follower id: " + follower_id)
        print("username: " + followersData[follower_id]["username"])
        print("access token: " + followersData[follower_id]["access_token"])
        for repo in followersData[follower_id]["repos"]:
            print("repo: " + repo)
            results = getNewEvents(repo, followersData[follower_id]["username"], followersData[follower_id]["access_token"])
            if(len(results) != 0):
                print("ada event baru")
                for result in results:
                    string_to_chat = "[" + repo + "] " +  result["commit"]["committer"]["name"] + " melakukan " + result["commit"]["message"] + " pada waktu " + result["commit"]["committer"]["date"]
                    print(string_to_chat)
                    chatToFollower(follower_id, string_to_chat)
            else:
                print("tidak ada event baru")
                # chatToFollower(follower_id, "tidak ada event baru")

def chatToFollower(follower_id, string_to_send):
    line_bot_api.push_message(follower_id, TextSendMessage(text=string_to_send))


def getNewEvents(repo, username, access_token):
    # repo sama username buat ngeidentifikasi repo yang mana yang mo disentuh
    # return array of new event(new disini artinya event tersebut dilakukan selama interlude). kalo ga ada, return empty array
    url = 'https://api.github.com/repos/' + username + '/' + repo + '/commits'
    # print("url: " + url)
    headers = {'Authorization': 'token ' + access_token}
    res_json = requests.get(url, headers=headers)
    res_dicts = json.loads(res_json.text)
    # print("banyak event sampe saat ini:", len(res_dicts))
    start_time = datetime.now(pytz.utc).replace(tzinfo=None) 
    
    # print("waktu sekarang", start_time)
    # iterasi setiap response, jika ada response yang dibuat < 5 menit terakhir, add to results
    results = []
    for res in res_dicts:
        # print("res")
        # print(res)
        # print("event di waktu:" + res["commit"]["committer"]["date"])
        # ambil waktu dari res
        #  "created_at": "2022-05-25T05:58:32Z"
        event_time = datetime.strptime(res["commit"]["committer"]["date"], '%Y-%m-%dT%H:%M:%SZ')
        diff = start_time - event_time
        # print("diff.total_seconds() = ")
        # print(diff.total_seconds())
        if (diff.total_seconds() <= interlude):
            print("ada commit baru!")
            results.append(res)
    return results
