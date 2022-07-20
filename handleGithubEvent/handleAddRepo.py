import globalVariable
from utils.firebaseUtils import setFirebaseFromDatabase
def handleAddRepo(groupId, hookId, username, repo):
    globalVariable.database["active"][groupId] = {hookId: {"username": username, "repo": repo}}
    setFirebaseFromDatabase()
    # update database, trus update firebase
    pass