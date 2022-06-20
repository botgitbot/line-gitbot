
from globalVariable import database
from lineUtils import replyString
# udah gada campur tangan sama flask
def replyBasedOnMessage(msg_from_user, source_type, followers_id, reply_token):

    if source_type == 'user':
        replyString(reply_token, "Line gitbot is only available for group chat.")
        return

    if msg_from_user=="test": # memastikan flask berjalan dengan aman
        replyString(reply_token, "coba github api!")
    elif msg_from_user[0:9] == '!addrepo ': # catet username, repo, and access token. Format ![repo]/[username]:[access_token] untuk pertama kali
        if msg_from_user[9:].find("/") != -1 and msg_from_user[8:].find(":") != -1:
            username = msg_from_user[9:msg_from_user.find("/")]
            repo = msg_from_user[msg_from_user.find("/")+1:msg_from_user.find(":")]
            access_token = msg_from_user[msg_from_user.find(":")+1:]
            group_id = followers_id

            replyString(reply_token, "username: " + username + "\nrepo: " + repo + "\naccess token: " + access_token)
            user_and_repo_name_as_key = username + "/" + repo

            if (group_id in list(database.keys())):
                database[group_id][user_and_repo_name_as_key] = {"access_token": access_token}
            else:
                database[group_id] = {user_and_repo_name_as_key: {"access_token": access_token}}

    elif msg_from_user == '!help': #help
        replyString(reply_token, "add first repo with `!addrepo [owner]/[repo]:[access_token]`\nhelp with `!help`")

