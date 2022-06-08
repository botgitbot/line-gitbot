'''
    IMPORT
'''
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

'''
    CREATE FLASK
'''

app = Flask(__name__)

'''
    GLOBAL VARIABLE
'''

line_bot_api = LineBotApi('hBs3vE924/xltPVsO3ef+5Jz0Fn7nCUS7LiDlaoI9C89tMv0oha23N/BpyV4yrKmCtdP0VuBTPNuXTLjse7yGNdqSdb9+iOk9M0SHfZOhLzbcdQzB/LP4oDiEVxKz6BOp0X+lZ2noXKdwvY/Pj44BwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f85e13929825bf9df787c225af107155')

repo = "test-line-bot"
username = "addinnabilal"

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
    global var
    global arrOfNumber
    global repo
    global username

    # ALGORITHM
    
    # get message yang diketikin sama user. simpen ke dalem variable msg_from_user
    msg_from_user = event.message.text
    
    # do something dengan bergantung sama messsage yang di chat sama user.
    if msg_from_user=="test": # memastikan flask berjalan dengan aman
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="coba github api!"))

    elif msg_from_user[0] == "!" and msg_from_user[1] == "r": # catet repo 
        # karakter selanjutnya adalah reponya
        repo = msg_from_user[2:]
        message = TextSendMessage(text = "repo:"+ repo)
        line_bot_api.reply_message(event.reply_token, message)
    
    elif msg_from_user[0] == "!" and msg_from_user[1] == "u": # catet username
        # karakter selanjutnya adalah username
        username = msg_from_user[2:]
        message = TextSendMessage(text = "username: " + username)
        line_bot_api.reply_message(event.reply_token, message)
    elif msg_from_user == "getevents":
        results = getNewEvents(repo, username)
        print("result yg baru:")
        for result in results:
            print(result["commit"]["committer"]["name"] + " melakukan " + result["commit"]["message"] + " pada waktu " + result["commit"]["committer"]["date"])

        message = TextSendMessage(text="cek console!")
        line_bot_api.reply_message(event.reply_token, message)
    else: 
        message = TextSendMessage(text="bukan command khusus!")
        line_bot_api.reply_message(event.reply_token, message)


'''
    HELPER FUNCTION
'''

def getNewEvents(repo, username):
    # repo sama username buat ngeidentifikasi repo yang mana yang mo disentuh
    # return array of new event. kalo ga ada, return empty array
    url = 'https://api.github.com/repos/' + username + '/' + repo + '/commits'
    print("url: " + url)
    res_json = requests.get(url)
    res_dicts = json.loads(res_json.text)
    print("banyak event sampe saat ini:", len(res_dicts))
    start_time = datetime.now(pytz.utc)
    
    print("waktu sekarang", start_time)
    # iterasi setiap response, jika ada response yang dibuat < 5 menit terakhir, add to results
    results = []
    for res in res_dicts:
        print("event di waktu:" + res["commit"]["committer"]["date"])
        # ambil waktu dari res
        #  "created_at": "2022-05-25T05:58:32Z"
        event_time = datetime.strptime( res["commit"]["committer"]["date"], '%Y-%m-%dT%H:%M:%SZ')
        diff = start_time - event_time
        print("diff.total_seconds() = ")
        print(diff.total_seconds())
        if (diff.total_seconds() <= 600):
            print("diff:" + str(diff))
            results.append(res)
    return results
    




print("testing")



'''
    FUNCTION TO RUN EVERY MINUTE
'''

# import time
# import atexit

# from apscheduler.schedulers.background import BackgroundScheduler


# def print_date_time():
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


# scheduler = BackgroundScheduler()

# scheduler.add_job(func=print_date_time, trigger="interval", seconds=10)

# scheduler.start()

# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())
print("testing2")

'''
    RUN FLASK APP
'''

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)