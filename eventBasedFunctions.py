
from firebaseUtils import setDatabaseFromFirebase, setFirebaseFromDatabase
import globalVariable
from lineUtils import replyString, replyFlexMessage
from utils import checkIfRepoAndAccessTokenValid
# udah gada campur tangan sama flask
def actionBasedOnMessage(msg_from_user, source_type, followers_id, reply_token):
    if source_type == 'user':
        replyString(reply_token, "Line gitbot is only available for group chat.")
        return
    
    if msg_from_user[0] == '!':
        # sanitize msg_from_user
        # delete spaces in the back, and remove spaces that is more than one
        msg_from_user = msg_from_user.strip()
        msg_from_user = ' '.join(msg_from_user.split())
        print("santized msg_from_user")
        print(msg_from_user)


        if msg_from_user[0:5] == '!add ': #intentional space behind
            actionAddRepo(reply_token, msg_from_user, followers_id)
        
        elif msg_from_user == '!show':
            actionShowRepo(reply_token, followers_id)

        elif msg_from_user[0:8] == '!delete ':
            actionDeleteRepo(reply_token, msg_from_user, followers_id)
        

        elif msg_from_user == '!help': #help
            actionSendHelp(reply_token)
        elif msg_from_user == '!testflex':
            actionFlex(reply_token);







def actionDeleteRepo(reply_token, msg_from_user, group_id):
    # catet username, repo, and access token. Format ![repo]/[username]
    if msg_from_user[12:].find("/") != -1:
        username = msg_from_user[12:msg_from_user.find("/")]
        repo = msg_from_user[msg_from_user.find("/")+1:]
        # check if key available
        user_and_repo_name_as_key = username + "@" + repo

        # cek apakah group id ada (artinya sudah eprnah nambahin repo), dan repo tersebut ada di group id tersebut. kalo keduanya aman, artinya bisa delete repo
        if group_id in list(globalVariable.database.keys()) and user_and_repo_name_as_key in list(globalVariable.database[group_id].keys()):
            globalVariable.database[group_id].pop(user_and_repo_name_as_key)
            setFirebaseFromDatabase()
            replyString(reply_token, "successfully deleting \nusername: " + username + "\nrepo: " + repo)
        else:
            replyString(reply_token, "you haven't added " + username + "/" + repo + " yet")
        
    else:
        replyString(reply_token, "wrong format, please use\n `!deleterepo [owner]/[repo]`")

        user_and_repo_name_as_key = username + "@" + repo
    if msg_from_user[12:].find("/") != -1 and msg_from_user[11:].find(":") != -1:
        username = msg_from_user[12:msg_from_user.find("/")]
        repo = msg_from_user[msg_from_user.find("/")+1:msg_from_user.find(":")]
        access_token = msg_from_user[msg_from_user.find(":")+1:]
        

        user_and_repo_name_as_key = username + "@" + repo

def actionShowRepo(reply_token, group_id):
    if group_id in list(globalVariable.database.keys()):
        stringToSend = ""
        for key in globalVariable.database[group_id]:
            stringToSend += "-" + key.replace("@", "/") + "\n"
        replyFlexMessage(reply_token, {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "Repository list in this group:",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": stringToSend,
                    "wrap": True
                }
                ],
                "backgroundColor": "#EFEFEF"
            }
            })
    else:
        replyString(reply_token, "no repo added yet")


def actionSendHelp(reply_token):
    replyString(reply_token, """
    add first repo with
    `!add [owner]/[repo]:[access_token]`

    help with
    `!help` 

    show repo list with
    `!show`

    delete repo with
    `!delete [owner]/[repo]`
    """)

def actionAddRepo(reply_token, msg_from_user, group_id):
    # catet username, repo, and access token. Format ![repo]/[username]:[access_token]
    if msg_from_user[9:].find("/") != -1 and msg_from_user[8:].find(":") != -1:
        username = msg_from_user[9:msg_from_user.find("/")]
        repo = msg_from_user[msg_from_user.find("/")+1:msg_from_user.find(":")]
        access_token = msg_from_user[msg_from_user.find(":")+1:]
        

        user_and_repo_name_as_key = username + "@" + repo
        # user_and_repo_name_as_key = {"username": username, "repo": repo}
        print("globalVariable.database prev")
        # replyString(reply_token, "adding...")

        # check if the data sended is valid. try to get data from github
        # if not valid, reply with error message
        # if valid, add to database
        if not checkIfRepoAndAccessTokenValid(username+"/"+repo, access_token):
            replyString(reply_token, "invalid repo or access token")
        else:
            print(globalVariable.database)
            if (group_id in list(globalVariable.database.keys())):
                globalVariable.database[group_id][user_and_repo_name_as_key] = {"access_token": access_token}
            else:
                globalVariable.database[group_id] = {user_and_repo_name_as_key: {"access_token": access_token}}
            print("globalVariable.database edited")
            print(globalVariable.database)
            # set to firebase
            setFirebaseFromDatabase()
            replyString(reply_token, "successfully adding \nusername: " + username + "\nrepo: " + repo + "\naccess token: " + access_token)
    else:
        replyString(reply_token, "wrong format, please use\n `!addrepo [owner]/[repo]:[access_token]`")
           

def actionFlex(reply_token):
    replyFlexMessage(reply_token, {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "nama repo",
                    "decoration": "underline",
                    "contents": []
                },
                {
                    "type": "text",
                    "text": "isi messagenya",
                    "style": "italic"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "uri",
                        "label": "click me",
                        "uri": "https://github.com/addinnabilal/server-line-bot"
                        },
                        "style": "link",
                        "color": "#858383"
                    }
                    ],
                    "paddingAll": "5px"
                }
                ],
                "borderColor": "#965d5d",
                "backgroundColor": "#d1d1d1"
            }
        })
