# import globalVariable
from utils.lineUtils import replyFlexMessageTemplateTitleText, replyString
import globalVariable
from config import exampleKey
def handleShowRepo(reply_token, group_id):
    # replyString(reply_token, "showrepo is not yet implemented")




    if group_id in list(globalVariable.database["active"].keys()):
        stringToSend = ""
        for webhookId in globalVariable.database["active"][group_id]:
            if(webhookId != exampleKey):
                username = globalVariable.database["active"][group_id][webhookId]["username"]
                repo = globalVariable.database["active"][group_id][webhookId]["repo"]
                stringToSend += username + " / " + repo + "\n"
        if(stringToSend == ""):
            replyString(reply_token, "no repo added yet")
        else:
            replyFlexMessageTemplateTitleText(reply_token, "Repository list in this group: ", stringToSend)
    else:
        replyString(reply_token, "no repo added yet")
