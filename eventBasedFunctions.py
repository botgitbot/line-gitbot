
from globalVariable import database

# udah gada campur tangan sama flask
def replyBasedOnMessage(msg_from_user):
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
    elif msg_from_user == '#help': #help
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="add first repo with `![repo]/[username]:[access_token]`\nadd another repo with `+[repo]`\nhelp with `#help`"))


    else: 
        message = TextSendMessage(text="bukan command khusus!")
        line_bot_api.reply_message(event.reply_token, message)