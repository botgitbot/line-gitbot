import globalVariable
from utils.lineUtils import replyFlexMessage, replyString
from utils.utils import keyToUsernameAndRepo

def actionShowRepo(reply_token, group_id):
    if group_id in list(globalVariable.database.keys()):
        stringToSend = ""
        for key in globalVariable.database[group_id]:
            username, repo = keyToUsernameAndRepo(key)
            stringToSend += username + "/" + repo + "\n"
        replyFlexMessage(reply_token, {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "Repository list in this group:",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": stringToSend,
                    "wrap": True
                }
                ],
                "backgroundColor": "#EFEFEF"
            }
            })
    else:
        replyString(reply_token, "no repo added yet")
