'''
    IMPORT
'''
from cmath import e
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import requests
import json
from datetime import datetime
import pytz
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

'''
    CREATE FLASK
'''

app = Flask(__name__)

'''
    GLOBAL VARIABLE
'''

line_bot_api = LineBotApi('hBs3vE924/xltPVsO3ef+5Jz0Fn7nCUS7LiDlaoI9C89tMv0oha23N/BpyV4yrKmCtdP0VuBTPNuXTLjse7yGNdqSdb9+iOk9M0SHfZOhLzbcdQzB/LP4oDiEVxKz6BOp0X+lZ2noXKdwvY/Pj44BwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f85e13929825bf9df787c225af107155')
interlude = 10

followersData = {}
    # "U195dcbc6b51ab6056d2f9a9c5dfde093":
    #     {"repos": ["test-line-bot"], "username": "addinnabilal", "access_token": "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"}},

'''
    FLASK FUNCTION
'''

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



# handle message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # KAMUS
    global repo
    global username
    global access_token

    # ALGORITHM
    
    # get message yang diketikin sama user. simpen ke dalem variable msg_from_user
    msg_from_user = event.message.text
    followers_id = event.source.user_id

    # do something dengan bergantung sama messsage yang di chat sama user.
    if msg_from_user=="test": # memastikan flask berjalan dengan aman
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="coba github api!"))

    elif msg_from_user[0] == "!": # catet username, repo, and access token. Format ![repo]/[username]:[access_token] untuk pertama kali
        if msg_from_user[1:].find("/") != -1 and msg_from_user[1:].find(":") != -1:
            username = msg_from_user[1:msg_from_user.find("/")]
            repo = msg_from_user[msg_from_user.find("/")+1:msg_from_user.find(":")]
            # catat access token
            access_token = msg_from_user[msg_from_user.find(":")+1:]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="username: " + username + "\nrepo: " + repo + "\naccess token: " + access_token)) 

            followersData[followers_id] = {"repos": [repo], "username": username, "access_token": access_token}

    elif msg_from_user[0] ==  "+": #catat tambahan repo
        if len(followersData[followers_id]["repos"]) != 0: #asumsi data user sudah terdefinisi sebelumnya
            followersData[followers_id]["repos"].append(msg_from_user[1:])

    else: 
        message = TextSendMessage(text="bukan command khusus!")
        line_bot_api.reply_message(event.reply_token, message)


'''
    HELPER FUNCTION
'''
def checkAllFollowersRepo():
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
    # return array of new event. kalo ga ada, return empty array
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


'''
    FUNCTION TO RUN EVERY MINUTE
'''


scheduler = BackgroundScheduler()

scheduler.add_job(func=checkAllFollowersRepo, trigger="interval", seconds = interlude)

scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

'''
    RUN FLASK APP
'''

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)