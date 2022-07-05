import globalVariable
from utils.lineUtils import replyFlexMessage, replyString, replyFlexMessageTemplateTitleText
from utils.utils import keyToUsernameAndRepo

def actionShowRepo(reply_token, group_id):
    if group_id in list(globalVariable.database.keys()):
        stringToSend = ""
        for key in globalVariable.database[group_id]:
            username, repo = keyToUsernameAndRepo(key)
            stringToSend += username + "/" + repo + "\n"
        replyFlexMessageTemplateTitleText(reply_token, "Repository list in this group: ", stringToSend)
    else:
        replyString(reply_token, "no repo added yet")
