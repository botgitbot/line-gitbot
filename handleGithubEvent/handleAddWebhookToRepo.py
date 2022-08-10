import globalVariable
from utils.firebaseUtils import setFirebaseFromDatabase
from utils.lineUtils import sendStringToGroup
from utils.utils import addWebhookToDatabase
def handleAddWebhookToRepo(group_id, hook_id, username, repo):
    print("hook_id baru = " + str(hook_id))
    addWebhookToDatabase(group_id, hook_id, username, repo)
    sendStringToGroup(group_id, username +"/" + repo + " is now tracked!")

    # update database, trus update firebase