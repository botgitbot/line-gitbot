import globalVariable
from utils.firebaseUtils import setFirebaseFromDatabase
from utils.lineUtils import sendStringToGroup
def handleAddWebhookToRepo(group_id, hookId, username, repo):
    globalVariable.database["active"][group_id] = {hookId: {"username": username, "repo": repo}}
    setFirebaseFromDatabase()
    sendStringToGroup(group_id, username +"/" + repo + " is now tracked!")

    # update database, trus update firebase