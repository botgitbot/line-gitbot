import globalVariable
from utils.lineUtils import replyString
from utils.firebaseUtils import setFirebaseFromDatabase
from config import exampleKey
def handleManualDelete(reply_token, group_id, msg_from_user):
    try:
        usernameAndRepo = msg_from_user[14:].split("/")
        username = usernameAndRepo[0]
        repo = usernameAndRepo[1]
        print(username + " " + repo)
    except:
        replyString(reply_token, "invalid syntax")
        return
    if(username == "" or repo == ""):
        replyString(reply_token, "invalid syntax")
        return
    if(group_id in list(globalVariable.database["active"].keys())):
        # check every webhook_id in database
        isFound = False
        for webhookId in globalVariable.database["active"][group_id]:
            if(webhookId != exampleKey):
                if(globalVariable.database["active"][group_id][webhookId]["username"] == username and globalVariable.database["active"][group_id][webhookId]["repo"] == repo):
                    isFound = True
                    # remove key from database
                    globalVariable.database["active"][group_id].pop(webhookId, None)
                    setFirebaseFromDatabase()
                    replyString(reply_token, "removed " + username + "/" + repo)
                    return
        if(not isFound):
            replyString(reply_token, "no repo found")
            return