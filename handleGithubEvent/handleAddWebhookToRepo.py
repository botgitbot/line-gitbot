import globalVariable
from utils.firebaseUtils import setFirebaseFromDatabase
from utils.lineUtils import sendStringToGroup
def handleAddWebhookToRepo(group_id, hook_id, username, repo):
    print("hook_id baru = " + str(hook_id))
    globalVariable.database["active"][group_id][hook_id] = {"username": username, "repo": repo}
    setFirebaseFromDatabase()
    sendStringToGroup(group_id, username +"/" + repo + " is now tracked!")

    # update database, trus update firebase