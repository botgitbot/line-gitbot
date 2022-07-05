from utils.firebaseUtils import setFirebaseFromDatabase
import globalVariable
from utils.lineUtils import replyString
from utils.utils import createKeyFromUsernameAndRepo


def actionDeleteRepo(reply_token,username, repo, group_id):
    # catet username, repo, and access token. Format ![repo]/[username]
 
    # check if key available
    user_and_repo_name_as_key = createKeyFromUsernameAndRepo(username, repo)

    # cek apakah group id ada (artinya sudah eprnah nambahin repo), dan repo tersebut ada di group id tersebut. kalo keduanya aman, artinya bisa delete repo
    if group_id in list(globalVariable.database.keys()) and user_and_repo_name_as_key in list(globalVariable.database[group_id].keys()):
        globalVariable.database[group_id].pop(user_and_repo_name_as_key)
        setFirebaseFromDatabase()
        replyString(reply_token, "successfully deleting \nusername: " + username + "\nrepo: " + repo)
    else:
        replyString(reply_token, "you haven't added " + username + "/" + repo + " yet")
    
 