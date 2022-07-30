import globalVariable
from utils.firebaseUtils import setFirebaseFromDatabase
from utils.lineUtils import sendStringToGroup

def handleDeleteRepoEvent(group_id, webhook_id, username, repo):
    # update database, trus update firebase
    # remove key from database
    globalVariable.database["active"][group_id].pop(webhook_id, None)
    setFirebaseFromDatabase()
    sendStringToGroup(group_id, username +"/" + repo + " is stopped being tracked!")