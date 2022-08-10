import globalVariable
from utils.firebaseUtils import setFirebaseFromDatabase
from utils.lineUtils import sendStringToGroup
from utils.utils import usernameAndRepoAsDatabaseKey

def handleDeleteRepoEvent(group_id, username, repo):
    # update database, trus update firebase
    # remove key from database
    urkey = usernameAndRepoAsDatabaseKey(username, repo)
    globalVariable.database["active"][group_id].pop(urkey, None)
    setFirebaseFromDatabase()
    sendStringToGroup(group_id, username +"/" + repo + " is stopped being tracked!")