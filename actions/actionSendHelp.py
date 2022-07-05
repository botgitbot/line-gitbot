
from utils.lineUtils import replyString, replyFlexMessageTemplateTitleText

def actionSendHelp(reply_token):
    replyFlexMessageTemplateTitleText(reply_token, "Command List", """
        add first repo with
        `!add [owner]/[repo]:[access_token]`

        help with
        `!help` 

        show repo list with
        `!show`

        delete repo with
        `!delete [owner]/[repo]`
        """)

        