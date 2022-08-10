import globalVariable
from utils.lineUtils import replyString
from utils.firebaseUtils import setFirebaseFromDatabase

def handleManualDelete(reply_token, group_id, msg_from_user):
    usernameAndRepo = msg_from_user[15:].split("/")
    username = usernameAndRepo[0]
    repo = usernameAndRepo[1]
    if(username == "" or repo == ""):
        replyString(reply_token, "invalid syntax")
        return
    if(group_id in list(globalVariable.database["active"].keys())):
        # check every webhook_id in database
        for webhookId in globalVariable.database["active"][group_id]:
            if(webhookId != "examplewebhook"):
                if(globalVariable.database["active"][group_id][webhookId]["username"] == username and globalVariable.database["active"][group_id][webhookId]["repo"] == repo):
                    # remove key from database
                    globalVariable.database["active"][group_id].pop(webhookId, None)
                    setFirebaseFromDatabase()
                    replyString(reply_token, "removed " + username + "/" + repo)
                    return