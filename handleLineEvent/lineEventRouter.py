
from actions.actionAddRepo import actionAddRepo
from actions.actionDeleteRepo import actionDeleteRepo
from actions.actionSendHelp import actionSendHelp
from actions.actionShowRepo import actionShowRepo
from utils.lineUtils import replyString
from utils.utils import sanitizeMessage, splitMessageRepoUsername, splitMessageRepoUsernameToken
# udah gada campur tangan sama flask
def lineEventRouter(msg_from_user, source_type, followers_id, reply_token):
    if source_type == 'user':
        replyString(reply_token, "Line gitbot is only available for group chat.")
        return
    
    if msg_from_user[0] == '!':
        msg_from_user = sanitizeMessage(msg_from_user)
        if msg_from_user[0:5] == '!add ': #intentional space behind
            try:
                username, repo, token = splitMessageRepoUsernameToken(msg_from_user[5:])
            except:
                replyString(reply_token, "wrong format, please use\n `!add [owner]/[repo]:[access_token]`")
                return
            actionAddRepo(reply_token, username, repo, token, followers_id)

        elif msg_from_user == '!show':
            actionShowRepo(reply_token, followers_id)

        elif msg_from_user == '!help':
            actionSendHelp(reply_token)