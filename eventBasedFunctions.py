
from globalVariable import database
from lineUtils import replyString
# udah gada campur tangan sama flask
def replyBasedOnMessage(msg_from_user,followers_id, reply_token):
    if msg_from_user=="test": # memastikan flask berjalan dengan aman
        replyString(reply_token, "coba github api!")


    elif msg_from_user[0] == "!": # catet username, repo, and access token. Format ![repo]/[username]:[access_token] untuk pertama kali
        if msg_from_user[1:].find("/") != -1 and msg_from_user[1:].find(":") != -1:
            username = msg_from_user[1:msg_from_user.find("/")]
            repo = msg_from_user[msg_from_user.find("/")+1:msg_from_user.find(":")]
            # catat access token
            access_token = msg_from_user[msg_from_user.find(":")+1:]
            replyString(reply_token, text="username: " + username + "\nrepo: " + repo + "\naccess token: " + access_token)

            database[followers_id] = {"repos": [repo], "username": username, "access_token": access_token}

    elif msg_from_user[0] ==  "+": #catat tambahan repo
        if len(database[followers_id]["repos"]) != 0: #asumsi data user sudah terdefinisi sebelumnya
            database[followers_id]["repos"].append(msg_from_user[1:])

    elif msg_from_user == '#help': #help
        replyString(reply_token, "add first repo with `![repo]/[username]:[access_token]`\nadd another repo with `+[repo]`\nhelp with `#help`")
    else: 
        replyString(reply_token, "bukan command khusus!")