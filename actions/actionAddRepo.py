from utils.firebaseUtils import setFirebaseFromDatabase
from utils.lineUtils import replyString
from utils.utils import checkIfRepoAndAccessTokenValid, createKeyFromUsernameAndRepo
import globalVariable

def actionAddRepo(reply_token, username, repo, access_token, group_id):
    user_and_repo_name_as_key = createKeyFromUsernameAndRepo(username, repo)
    # user_and_repo_name_as_key = {"username": username, "repo": repo}
    # print("globalVariable.database prev")
    # replyString(reply_token, "adding...")

    # check if the data sended is valid. try to get data from github
    # if not valid, reply with error message
    # if valid, add to database
    if not checkIfRepoAndAccessTokenValid(username+"/"+repo, access_token):
        replyString(reply_token, username + "/" + repo + " is a not valid or access token is not valid")
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
